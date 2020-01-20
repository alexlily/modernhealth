select pg_terminate_backend(pid) from pg_stat_activity where datname='modernhealth';
drop database if exists modernhealth;