/**
 * Project Safety Extension — Pi harness safety netting.
 *
 * This extension ports the Cursor harness safety netting (`.cursor/`) to Pi:
 *
 *   1. protect-pyproject  — gate agent edits to pyproject.toml
 *      (port of .cursor/hooks/protect-pyproject.py)
 *   2. rtk compaction     — rewrite bash commands through `rtk hook cursor`
 *      so tool output stays compact before it reaches the model context
 *      (port of the `rtk hook cursor` preToolUse hook in .cursor/hooks.json)
 *   3. HyperFrames rule   — inject .cursor/rules/hyperframes-adhd-creative.mdc
 *      when the user prompt is video-related (alwaysApply: false)
 *
 * Commands:
 *   /gates   — run all project quality gates
 *   /safety  — show the status of each active protection
 */

import {
	isToolCallEventType,
	type BeforeAgentStartEvent,
	type ExtensionAPI,
	type ExtensionContext,
	type ToolCallEvent,
} from "@earendil-works/pi-coding-agent";
import { spawn } from "node:child_process";
import * as fs from "node:fs";
import * as path from "node:path";

// ---------------------------------------------------------------------------
// 1. protect-pyproject (port of .cursor/hooks/protect-pyproject.py)
// ---------------------------------------------------------------------------

const PROTECTED_NAME = "pyproject.toml";

// Shell patterns that can rewrite pyproject.toml (not mere reads).
const SHELL_WRITE_HINTS = /(?:\b(?:tee|sed|perl|ruby|python3?|uv|poetry|pip|printf|mv|cp|rm|touch|truncate|ed)\b|\bcat\b.*>|>>?)/i;

/** Mirrors _targets_pyproject() in protect-pyproject.py. */
function targetsPyproject(rawPath: unknown): boolean {
	if (typeof rawPath !== "string" || rawPath.length === 0) return false;
	const norm = rawPath.replace(/\\/g, "/").replace(/\/+$/, "");
	const name = norm.split("/").pop() ?? norm;
	return name.toLowerCase() === PROTECTED_NAME;
}

/** Mirrors _shell_touches_pyproject() in protect-pyproject.py. */
function shellTouchesPyproject(command: string): boolean {
	if (!command.includes("pyproject.toml")) return false;
	if (SHELL_WRITE_HINTS.test(command)) return true;
	// Still ask if the command clearly redirects into pyproject.toml.
	return />{1,2}\s*["']?[^"'\s]*pyproject\.toml/.test(command);
}

/**
 * Decide the gate outcome for a pyproject.toml edit.
 * With UI: ask the user (matches Cursor's "ask" permission).
 * Without UI: block (fail closed, matches failClosed: true in hooks.json).
 */
async function gatePyproject(ctx: ExtensionContext, what: string): Promise<boolean> {
	const message = `The agent wants to modify the protected file \`${PROTECTED_NAME}\` (${what}). Approve this change?`;
	if (ctx.hasUI) {
		const ok = await ctx.ui.confirm(`Protect: ${PROTECTED_NAME}`, message);
		if (ok) return true;
		ctx.ui.notify(`Blocked edit to ${PROTECTED_NAME}`, "warning");
		return false;
	}
	// Non-interactive modes fail closed, exactly like failClosed: true in Cursor.
	return false;
}

// ---------------------------------------------------------------------------
// 2. rtk bash compaction (port of `rtk hook cursor`)
// ---------------------------------------------------------------------------

const rtkCache = new Map<string, string | undefined>();
const RTK_CACHE_MAX = 512;

/** Rewrite a bash command with `rtk hook cursor`; return undefined to keep it. */
async function rewriteWithRtk(command: string): Promise<string | undefined> {
	if (rtkCache.has(command)) return rtkCache.get(command);

	const rewritten = await runRtkHook(command);
	if (rtkCache.size >= RTK_CACHE_MAX) rtkCache.clear();
	rtkCache.set(command, rewritten);
	return rewritten;
}

function runRtkHook(command: string): Promise<string | undefined> {
	return new Promise((resolve) => {
		let child;
		try {
			child = spawn("rtk", ["hook", "cursor"], {
				stdio: ["pipe", "pipe", "pipe"],
				env: process.env,
			});
		} catch {
			resolve(undefined);
			return;
		}

		const payload = JSON.stringify({
			hook_event_name: "preToolUse",
			tool_name: "Bash",
			tool_input: { command },
		});

		let stdout = "";
		let stderr = "";
		const timer = setTimeout(() => {
			child.kill("SIGKILL");
			resolve(undefined);
		}, 10_000);

		child.stdout.on("data", (d) => (stdout += d));
		child.stderr.on("data", (d) => (stderr += d));
		child.on("error", () => {
			clearTimeout(timer);
			resolve(undefined);
		});
		child.on("close", () => {
			clearTimeout(timer);
			try {
				const parsed = JSON.parse(stdout) as { updated_input?: { command?: string } };
				const updated = parsed.updated_input?.command;
				if (typeof updated === "string" && updated !== command) {
					resolve(updated);
					return;
				}
			} catch {
				// rtk returned non-JSON; leave the command untouched.
			}
			resolve(undefined);
		});

		child.stdin.on("error", () => {});
		child.stdin.write(payload, "utf-8");
		child.stdin.end();
	});
}

// ---------------------------------------------------------------------------
// 3. Cursor rule files → conditional system prompt injection
// ---------------------------------------------------------------------------

const VIDEO_PROMPT_HINTS = /hyperframes|video|animation|animate|render|explainer|promo\b|motion|storyboard|caption|captions|voiceover|voice-over|footage|slideshow|deck\b|narration|tts\b|movie|film|clip\b|title card|b-roll|broll/i;

/** Strip YAML frontmatter ("--- ... ---") from a Cursor .mdc rule file. */
function stripFrontmatter(content: string): string {
	const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(content);
	return match ? content.slice(match[0].length) : content;
}

function readRuleFile(cwd: string, relPath: string): string | undefined {
	try {
		const full = path.join(cwd, relPath);
		if (!fs.existsSync(full)) return undefined;
		return stripFrontmatter(fs.readFileSync(full, "utf-8")).trim();
	} catch {
		return undefined;
	}
}

// ---------------------------------------------------------------------------
// Gate runner (used by /gates)
// ---------------------------------------------------------------------------

interface GateResult {
	name: string;
	pass: boolean;
	durationSec: string;
	output: string;
}

interface GateSpec {
	name: string;
	cmd: string;
	args: string[];
	timeoutMs: number;
}

const GATES: GateSpec[] = [
	{ name: "ruff check", cmd: "uv", args: ["run", "ruff", "check", "app", "tests", "main.py"], timeoutMs: 180_000 },
	{ name: "ruff format", cmd: "uv", args: ["run", "ruff", "format", "--check", "app", "tests", "main.py"], timeoutMs: 180_000 },
	{ name: "ty (types)", cmd: "uv", args: ["run", "ty", "check"], timeoutMs: 300_000 },
	{ name: "complexipy", cmd: "uv", args: ["run", "complexipy"], timeoutMs: 300_000 },
	{ name: "radon gates", cmd: "uv", args: ["run", "python", "scripts/check_radon_gates.py"], timeoutMs: 300_000 },
	{
		name: "bandit",
		cmd: "uv",
		args: ["run", "bandit", "-c", "pyproject.toml", "-r", "app", "tests", "main.py", "--severity-level", "all", "--confidence-level", "all"],
		timeoutMs: 300_000,
	},
	{
		name: "semgrep",
		cmd: "uv",
		args: ["run", "semgrep", "scan", "--error", "--metrics=off", "--config", "p/owasp-top-ten", "--config", "p/security-audit", "--config", "p/python", "app", "tests", "main.py"],
		timeoutMs: 600_000,
	},
	{ name: "pytest (cov >= 90%)", cmd: "uv", args: ["run", "pytest"], timeoutMs: 900_000 },
];

function runGate(spec: GateSpec, cwd: string): Promise<GateResult> {
	return new Promise((resolve) => {
		const started = Date.now();
		let child;
		try {
			child = spawn(spec.cmd, spec.args, { cwd, env: process.env });
		} catch (err) {
			resolve({
				name: spec.name,
				pass: false,
				durationSec: "0.0",
				output: String(err),
			});
			return;
		}
		let output = "";
		let settled = false;

		const timer = setTimeout(() => {
			if (!settled) {
				settled = true;
				child.kill("SIGKILL");
				resolve({
					name: spec.name,
					pass: false,
					durationSec: ((Date.now() - started) / 1000).toFixed(1),
					output: `${output}\n[TIMEOUT after ${spec.timeoutMs} ms]`,
				});
			}
		}, spec.timeoutMs);

		child.stdout.on("data", (d) => (output += d));
		child.stderr.on("data", (d) => (output += d));
		child.on("error", (err) => {
			if (!settled) {
				settled = true;
				clearTimeout(timer);
				resolve({
					name: spec.name,
					pass: false,
					durationSec: ((Date.now() - started) / 1000).toFixed(1),
					output: String(err),
				});
			}
		});
		child.on("close", (code) => {
			if (!settled) {
				settled = true;
				clearTimeout(timer);
				resolve({
					name: spec.name,
					pass: code === 0,
					durationSec: ((Date.now() - started) / 1000).toFixed(1),
					output,
				});
			}
		});
	});
}

// ---------------------------------------------------------------------------
// Extension factory
// ---------------------------------------------------------------------------

export default function projectSafetyExtension(pi: ExtensionAPI) {
	// Cache rule file contents per session (they change rarely).
	let hyperframesRule: string | undefined;

	pi.on("session_start", (_event, ctx) => {
		hyperframesRule = readRuleFile(ctx.cwd, ".cursor/rules/hyperframes-adhd-creative.mdc");
	});

	// --- Safety gates on tool calls ----------------------------------------
	pi.on("tool_call", async (event: ToolCallEvent, ctx) => {
		// Reading pyproject.toml does not modify the protected file.
		if (isToolCallEventType("read", event) && targetsPyproject(event.input.path)) {
			return undefined;
		}

		// File-edit tools that can target pyproject.toml (no delete tool in pi).
		if (isToolCallEventType("write", event) || isToolCallEventType("edit", event)) {
			if (targetsPyproject(event.input.path)) {
				const allowed = await gatePyproject(ctx, `via ${event.toolName}`);
				if (!allowed) {
					return {
						block: true,
						reason: `Editing ${PROTECTED_NAME} requires explicit user approval. Do not retry until the user approves this change.`,
					};
				}
			}
			return undefined;
		}

		// Shell commands that may rewrite pyproject.toml.
		if (isToolCallEventType("bash", event)) {
			const command = event.input.command ?? "";
			if (shellTouchesPyproject(command)) {
				const allowed = await gatePyproject(ctx, "via a shell command");
				if (!allowed) {
					return {
						block: true,
						reason: `A shell command may modify ${PROTECTED_NAME}. The user did not approve it.`,
					};
				}
			}

			// rtk compaction (only after the pyproject gate passes).
			const rewritten = await rewriteWithRtk(command);
			if (rewritten) {
				event.input.command = rewritten;
			}
			return undefined;
		}

		return undefined;
	});

	// --- Conditional Cursor rules -------------------------------------------
	pi.on("before_agent_start", (event: BeforeAgentStartEvent) => {
		const additions: string[] = [];

		// HyperFrames rule: alwaysApply: false in Cursor → inject only when relevant.
		if (hyperframesRule && VIDEO_PROMPT_HINTS.test(event.prompt)) {
			additions.push(`## Project rule (video work) — HyperFrames ADHD-friendly defaults\n\n${hyperframesRule}`);
		}

		if (additions.length === 0) return undefined;
		return { systemPrompt: `${event.systemPrompt}\n\n${additions.join("\n\n")}` };
	});

	// --- /gates command ------------------------------------------------------
	pi.registerCommand("gates", {
		description: "Run all project quality gates (ruff, ty, complexipy, radon, bandit, semgrep, pytest)",
		handler: async (_args, ctx) => {
			const results: GateResult[] = [];
			ctx.ui.setStatus("gates", "running quality gates...");

			for (const spec of GATES) {
				ctx.ui.setStatus("gates", `running: ${spec.name}`);
				const result = await runGate(spec, ctx.cwd);
				results.push(result);
				ctx.ui.setWidget(
					"gates",
					results.map((r) => `${r.pass ? "PASS" : "FAIL"}  ${r.name}  (${r.durationSec}s)`),
				);
			}

			ctx.ui.setStatus("gates", undefined);
			const failed = results.filter((r) => !r.pass);

			if (failed.length === 0) {
				ctx.ui.notify(`All ${results.length} quality gates passed`, "info");
			} else {
				ctx.ui.notify(`Quality gates failed: ${failed.map((f) => f.name).join(", ")}`, "error");
			}

			// Keep the full log for inspection.
			try {
				const logPath = path.join(ctx.cwd, ".pi", "gates-last.log");
				const log = results
					.map((r) => `===== ${r.name} [${r.pass ? "PASS" : "FAIL"}] (${r.durationSec}s) =====\n${r.output}`)
					.join("\n\n");
				fs.writeFileSync(logPath, log, "utf-8");
			} catch {
				// Log file is best-effort.
			}
		},
	});

	// --- /safety command -----------------------------------------------------
	pi.registerCommand("safety", {
		description: "Show the status of each active Pi safety protection",
		handler: async (_args, ctx) => {
			const cwd = ctx.cwd;
			const lines: string[] = [];

			const ruleExists = (rel: string) => fs.existsSync(path.join(cwd, rel));
			const precommitExists = fs.existsSync(path.join(cwd, ".pre-commit-config.yaml"));
			const precommitInstalled =
				fs.existsSync(path.join(cwd, ".git", "hooks", "pre-commit")) ||
				fs.existsSync(path.join(cwd, ".git", "hooks", "pre-push"));

			lines.push("--- Pi safety netting ---");
			lines.push(`[${hyperframesRule ? "ON" : "OFF"}] HyperFrames rule (conditional) .cursor/rules/hyperframes-adhd-creative.mdc`);
			lines.push(`[ON] pyproject.toml protection      .pi/extensions/project-safety.ts`);
			lines.push(`[${rtkAvailable() ? "ON" : "OFF"}] rtk output compaction        ${rtkAvailable() ? "rtk on PATH" : "rtk NOT on PATH"}`);
			lines.push(`[${ruleExists("AGENTS.md") ? "ON" : "OFF"}] AGENTS.md operating manual`);
			lines.push(`[${precommitExists ? "ON" : "OFF"}] pre-commit config             .pre-commit-config.yaml`);
			lines.push(`[${precommitInstalled ? "ON" : "OFF"}] pre-commit hooks installed   .git/hooks/`);
			lines.push("");
			lines.push("/gates  runs the full quality suite");
			lines.push("/safety shows this status panel");

			ctx.ui.setWidget("safety", lines);
			ctx.ui.notify("Safety netting is active", "info");
		},
	});
}

function rtkAvailable(): boolean {
	try {
		// Cheap PATH probe; rtk lives under ~/.local/bin which is on PATH here.
		return process.env.PATH?.split(path.delimiter).some((dir) => {
			try {
				return fs.existsSync(path.join(dir, "rtk"));
			} catch {
				return false;
			}
		}) ?? false;
	} catch {
		return false;
	}
}
