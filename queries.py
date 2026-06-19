from db_connection import get_connection
import pandas as pd


def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_top_skills():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_skill_demand_realtime
        ORDER BY job_count DESC
        LIMIT 15
    """)


def get_top_roles():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_role_demand_realtime
        ORDER BY job_count DESC
        LIMIT 15
    """)


def get_country_distribution():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_country_demand_realtime
        ORDER BY job_count DESC
    """)


def get_pipeline_health():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_pipeline_health
        ORDER BY last_run_time DESC
        LIMIT 1
    """)

def get_latest_snapshot():
    return run_query("""
        SELECT
            snapshot_date,
            skills
        FROM skillpulse.gold.gold_skill_daily_snapshot
        ORDER BY snapshot_date DESC
        LIMIT 1
    """)


def get_emerging_skills():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_emerging_skills
        ORDER BY
            realtime_demand / historical_demand DESC
        LIMIT 15
    """)

def get_top_companies():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_top_companies_realtime
        ORDER BY job_count DESC
        LIMIT 15
    """)

def get_skill_trends():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_skill_trends
    """)

def get_skill_role_demand():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_skill_role_demand
        ORDER BY job_count DESC
        LIMIT 100
    """)

def get_company_skill_demand():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_company_skill_demand
        ORDER BY job_count DESC
        LIMIT 100
    """)

def get_country_skill_mapping():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_country_skill_mapping_realtime
    """)

def get_all_skills():
    return run_query("""
        SELECT *
        FROM skillpulse.gold.gold_skill_demand_realtime
        ORDER BY skill
    """)

def get_pipeline_history():
    return run_query("""
        SELECT
            DATE(snapshot_timestamp) AS run_date,
            MAX(bronze_job_count) AS bronze_jobs,
            MAX(silver_job_count) AS silver_jobs,
            MAX(extracted_skills) AS extracted_skills,
            MAX(unique_skills) AS unique_skills
        FROM skillpulse.monitoring.pipeline_run_history
        GROUP BY DATE(snapshot_timestamp)
        ORDER BY run_date
    """)

def get_skill_snapshot_history():
    return run_query("""
        SELECT
            snapshot_date,
            skill,
            job_count
        FROM skillpulse.gold.gold_skill_daily_snapshot
        WHERE skill IN (
            'Python',
            'SQL',
            'AWS',
            'Databricks',
            'Machine Learning'
        )
        ORDER BY snapshot_date
    """)

def get_emerging_skills():

    return run_query("""

    WITH skill_daily AS (

        SELECT
            snapshot_date,
            skill,
            job_count,

            LAG(job_count)
            OVER (
                PARTITION BY skill
                ORDER BY snapshot_date
            ) AS prev_count

        FROM skillpulse.gold.gold_skill_daily_snapshot

    )

    SELECT
        skill,
        job_count,
        prev_count,

        ROUND(
            (
                (job_count-prev_count)
                * 100.0
            )
            /
            NULLIF(prev_count,0),
            2
        ) AS pct_change

    FROM skill_daily

    WHERE prev_count IS NOT NULL

    ORDER BY pct_change DESC

    LIMIT 10

    """)

def get_alerts():

    return run_query("""
        SELECT
            alert_time,
            alert_type,
            severity,
            message
        FROM skillpulse.monitoring.alert_events
        ORDER BY alert_time DESC
        LIMIT 20
    """)