# Database Migration Decision

After evaluating scalability and flexibility, we decided to move from MongoDB to PostgreSQL.

## Reasons:
- Need for relational integrity
- Better support for analytics queries
- Team familiarity with SQL

## Considered Alternatives:
- Staying with MongoDB + Aggregations
- Using Firebase for faster prototyping

Final Decision: PostgreSQL hosted on Supabase
