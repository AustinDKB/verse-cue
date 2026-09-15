# Chapter 14: Doing the Right Thing

## Core Idea
Data systems shape decisions, opportunities, and power. Technical reliability does not guarantee social benefit. Predictive models can reproduce bias, feedback loops can amplify unequal treatment, and data collection can reduce privacy and freedom of choice.

Responsible design treats people as affected parties, not only as data subjects. It asks who benefits, who bears risk, who can challenge a decision, and whether the system can be limited, audited, corrected, or stopped.

## Frameworks Introduced

- **Predictive analytics as a decision system**
  - **When to use**: Apply this frame whenever a model ranks, filters, approves, denies, or allocates resources.
  - **How**: Define the decision and its impact. Identify the data source, target, proxy variables, error costs, and affected groups. Test outcomes, not only model accuracy.
  - **Trade-off**: A model can improve aggregate accuracy while increasing harm for a group with less data or less power.

- **Bias and discrimination**
  - **When to use**: Use this analysis before deployment and after changes in data, policy, or population.
  - **How**: Check representation, label quality, measurement bias, proxy features, disparate error rates, and unequal access to appeal. Compare treatment and outcomes across relevant groups.
  - **Boundary**: Removing a sensitive attribute does not remove its proxies or historical bias.

- **Feedback loops**
  - **When to use**: Use this frame when system outputs change future observations or behavior.
  - **How**: Map the loop from prediction to action to new data. Check whether early errors receive more reinforcement and whether the system can explore alternatives.

- **Privacy and tracking**
  - **When to use**: Use data minimization and purpose limits whenever collection can identify, profile, or influence a person.
  - **How**: Collect only needed data. State the purpose. Limit retention and access. Give people meaningful control. Assess re-identification risk in combined datasets.

- **Consent and freedom of choice**
  - **When to use**: Use this frame for terms, defaults, notifications, recommendations, and data sharing.
  - **How**: Make material effects clear before action. Avoid coercive defaults and dark patterns. Give a practical refusal, correction, export, and deletion path where policy permits.

- **Responsibility and accountability**
  - **When to use**: Use it when an automated result affects a person or public institution.
  - **How**: Assign a responsible owner. Record inputs, model or rule versions, decisions, and appeals. Make a human able to review and correct the result.

- **Legislation and self-regulation**
  - **When to use**: Use both legal and voluntary controls as design constraints, not as after-the-fact paperwork.
  - **How**: Track applicable rights and duties. Create internal review, audit, incident response, and sunset processes. Do not assume legal compliance proves ethical use.

## Key Concepts

- **Predictive analytics**: Analysis that estimates a future outcome or classification.
- **Bias**: A systematic error or unequal effect in data, measurement, or decision.
- **Discrimination**: Unequal treatment or outcome that harms a protected or vulnerable group.
- **Feedback loop**: A cycle in which an output changes the future input or outcome.
- **Privacy**: Control over personal information and the conditions of its use.
- **Tracking**: Recording activity across time, places, devices, or services.
- **Surveillance**: Monitoring people or behavior to observe, classify, or control.
- **Consent**: A meaningful choice made with enough information about material use.
- **Data minimization**: Collecting and retaining no more personal data than needed.
- **Accountability**: A clear duty to explain, correct, and answer for system effects.
- **Auditability**: Evidence that allows a decision and its inputs to be reviewed.

## Mental Models

- Treat data as a source of power, not as a neutral asset.
- Treat an automated prediction as an intervention when it changes a person's options.
- Treat accuracy as one metric among error distribution, recourse, privacy, and social impact.
- Treat consent as ongoing control, not a single click hidden in a long notice.
- Treat historical data as a record of past institutions, not an objective description of merit.

## Anti-patterns

- **Use accuracy as the only fairness test**: Aggregate accuracy can hide unequal errors and unequal harm.
- **Remove sensitive fields and declare neutrality**: Proxy variables and historical patterns can preserve discrimination.
- **Collect data because storage is cheap**: Extra data increases misuse, breach, inference, and retention risk.
- **Use opaque defaults for material choices**: A nominal choice can become coercion when refusal is costly.
- **Automate high-impact decisions without appeal**: People need a path to correction when data or rules are wrong.
- **Treat legal permission as sufficient justification**: A permitted use can still harm people or weaken autonomy.

## Reference Tables

| Question | Evidence to collect | Design response |
|---|---|---|
| Who is affected? | Groups, power, access, downstream use | Include affected parties in review |
| What data drives the result? | Sources, labels, proxies, retention | Minimize, document, and limit use |
| What can go wrong? | Error rates, feedback, misuse | Add tests, safeguards, and monitoring |
| Can a person challenge it? | Explanation, appeal, correction | Provide human review and a remedy |
| Who answers for harm? | Owner, vendor, operator | Assign accountability and audit logs |

| Risk | Fast tell | Needed control |
|---|---|---|
| Bias | Output differs by group without a justified reason | Outcome and error analysis |
| Feedback loop | Decisions change the future training data | Exploration and loop monitoring |
| Privacy loss | Data combines across purposes or contexts | Purpose limits and minimization |
| Loss of autonomy | Refusal is hidden or costly | Clear choice and practical exit |

## Worked Example

A service predicts which applications need extra review. If reviewers inspect only predicted high-risk cases, later records contain more labels from that group. The model then sees the concentrated review data as evidence that the group is high risk. This feedback loop can grow even if the first model was only slightly biased.

A responsible design measures error and review rates across groups, records the policy and model versions, samples cases outside the predicted group, provides an appeal path, and sets a review date. It also limits retention and access to the data used for the decision.

## Key Takeaways

1. Ask who gains power and who bears risk before building a data feature.
2. Test unequal outcomes, proxies, feedback loops, privacy, and recourse.
3. Minimize data collection and limit each use to a stated purpose.
4. Give people clear choices and a practical correction path.
5. Record decision inputs, versions, owners, and appeals for auditability.
6. Treat legal, ethical, and operational review as part of system design.

## Connects To

- **Chapter 1**: Architecture choices carry legal and social consequences.
- **Chapter 5**: Schema and dataflow decisions shape retention and disclosure.
- **Chapter 9**: Audit and fault models help expose unsafe system behavior.
- **Chapter 13**: Derived data and feedback loops need end-to-end accountability.
