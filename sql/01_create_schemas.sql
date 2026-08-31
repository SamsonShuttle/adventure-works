-- Active: 1788173561694@@127.0.0.1@5432@adventure_works
-- Run while connected to the adventure_works database.

CREATE SCHEMA IF NOT EXISTS ingest; -- Used as a log of the pipeline runs
CREATE SCHEMA IF NOT EXISTS staging; -- The raw data aka 'Bronze layer'
CREATE SCHEMA IF NOT EXISTS core; -- Cleaning the data and normalizing it aka 'Silver layer'
CREATE SCHEMA IF NOT EXISTS marts; -- Dim/Fact tables ready for Power BI aka 'Gold layer'

