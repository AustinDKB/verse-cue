# Chapter 17: Kimball DW/BI Lifecycle Overview

## Core Idea
The **Kimball Lifecycle** is a roadmap for a DW/BI program from readiness assessment through deployment, maintenance, and growth. It joins business requirements, technology, data, and BI applications in manageable, iterative projects. The roadmap shows dependencies and concurrent work, not a fixed calendar.

## Frameworks Introduced
- **Kimball Lifecycle**: Use when planning or governing a DW/BI initiative. Start with program/project planning and business requirements definition. Then run three concurrent tracks: technical architecture and product selection, dimensional modeling and ETL, and BI application design and development. Converge the tracks at deployment, continue maintenance, and return to the beginning for each growth project.
- **Roadmap Mile Markers**: Use to assign work and dependencies. Assess readiness, scope and justify the initiative, define requirements, design the architecture, select products, model and physically design data, build ETL and BI applications, deploy, then maintain and grow the environment.
- **Hybrid requirements approach**: Use when business input must produce both detail and consensus. Conduct interviews to learn how people work, make decisions, measure success, and use reports. Follow interviews with facilitated sessions that bring participants to agreement.
- **Prioritization grid**: Use when more business processes need attention than one iteration can support. Place each process by potential business impact and feasibility. Start with high-impact, highly feasible work. Address high-impact but infeasible work through other efforts, defer low-impact feasible work, and avoid low-impact infeasible work.
- **Eight-step technical architecture design process**: Use to create an explicit architecture without delaying delivery. Establish an architecture task force. Collect and document architecture-related requirements. Create the architecture model. Determine implementation phases. Design and specify subsystems. Create the architecture plan. Review and finalize the plan. Use it to guide product selection.
- **Product evaluation matrix**: Use to select products against actual needs. Convert architecture requirements into specific criteria with weighting factors. Research the market, score a short list, involve business representatives for BI tools, and use references. If no clear winner emerges, prototype no more than two products with a limited, realistic business case.

## Key Concepts
- **Kimball Lifecycle**: An iterative DW/BI delivery and management roadmap that aligns business value, dimensional data, technology, and BI applications.
- **Business Dimensional Lifecycle**: The former name for the Kimball Lifecycle, emphasizing business needs, dimensional structures, and manageable projects.
- **Business sponsor**: The executive who has a clear vision, advocates for the initiative, and gains peer support.
- **Data feasibility**: The degree to which real, reasonably clean source data exists at the granularity required by business needs.
- **Opportunity/stakeholder matrix**: A matrix with business processes as rows and organizational groups or functions as columns, used to show cross-organization impact.
- **Bus matrix**: A blueprint that exposes common business processes and shared dimensions, supporting an extensible, integrated environment.
- **Technical architecture**: The explicit framework that integrates DW/BI technical services, infrastructure, applications, and planned implementation phases.
- **Physical design**: Translation of dimensional models into database structures, including naming standards, staging and audit tables, indexes, aggregates, partitions, and storage details.
- **Parameter-driven BI application**: A standardized analytic template that lets users vary parameters instead of starting each analysis from scratch.
- **Growth**: New users, data, applications, or major enhancements prioritized with the business and handled by returning to the Lifecycle.

## Mental Models
- Use business requirements as the filter for architecture and product choices. A product-first decision reverses the roadmap and creates technology without a business purpose.
- Treat the architecture as a communication blueprint. It must be explicit enough to coordinate parallel work, expose required phases, and support product evaluation.
- Treat deployment as a readiness decision, not a date commitment. Data quality, operations, performance, usability, education, and support must converge before release.
- View demand for growth as evidence of acceptance. Reuse the established technical, data, and BI foundations, then repeat the Lifecycle for new priorities.

## Anti-patterns
- **Technology-first design**: Selecting products before defining business needs leads to a tool-driven environment that cannot solve the right problems.
- **The Law of Too**: Avoid too short a timeline combined with too many source systems, users, locations, and analytic requirements. The scope becomes unmanageable.
- **Architecture bypass or architecture overreach**: Avoid both improvised components that later require rebuilding and a long architecture exercise detached from business delivery.
- **Requirements by survey or top-five reports**: Surveys cannot probe unexpected needs, and a fixed top-five list cannot support changing business questions.
- **Standalone dimensional models**: Do not build models without shared, conformed dimensions. Isolated structures prevent integration across processes.
- **Undercooked deployment**: Do not release unstable data to preserve a promised date. Users judge the system by data quality and will not return after a poor first experience.
- **Normalized-only delivery**: Do not spend the budget on normalized structures while omitting a usable dimensional presentation area.

## Worked Example
A requirement calls for global sales performance data every night. The architecture team records the requirement in a table with its implications rather than selecting a product immediately. The implications include 24/7 worldwide availability, data mirroring for loads, robust metadata for global access, sufficient network bandwidth, and enough ETL capacity for complex operational-data integration. The team groups these needs under ETL, BI, metadata, and infrastructure, places mandatory capabilities in the first implementation phase, and uses the resulting architecture plan as the product-evaluation basis. After deployment, the team monitors usage and performance, then adjusts indexes, aggregates, and storage as actual access patterns become clear.

## Key Takeaways
- Assess executive business sponsorship, compelling business motivation, and data feasibility before committing resources.
- Scope the first iteration around one meaningful business process and protect it from the Law of Too.
- Gather requirements through open-ended interviews, data-centric interviews, and facilitated consensus.
- Prioritize processes with the business by impact and feasibility, not in an IT vacuum.
- Build an explicit architecture from requirements, then select products that fit the architecture.
- Deliver a starter set of about 10 to 15 BI applications with shared standards and parameter-driven templates.
- Plan deployment, support, education, technical monitoring, and future growth as part of the Lifecycle.

## Connects To
- **Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer**: Connects the Lifecycle with agile methods, business value, and the bus architecture foundation.
- **Chapter 4: Inventory**: Supplies the enterprise data warehouse bus architecture, bus matrix, and data steward context.
- **Chapter 18: Dimensional Modeling Process and Tasks**: Details collaborative modeling workshops that follow requirements definition.
- **Chapters 19 and 20: ETL Subsystems and Techniques, and ETL System Design and Development Process and Tasks**: Expand the ETL track and its design tasks.
- **Fact table, dimension, and conformed dimension**: These dimensional modeling concepts support the data track that this chapter places within the larger Lifecycle.
