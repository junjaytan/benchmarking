/*
 * Various Redshift system table queries for getting stats on runtime, etc.
 *
 * You should run queries with specific labels in order for these queries to be most useful.
 */

 -- Query runtime summary (using labels)
 -- usually default userid is 100, though it may differ.
 select query, starttime, endtime, pid, userid, elapsed/1000 AS elapsed_msec, elapsed::DECIMAL/1000000 as elapsed_sec, label, aborted, substring
 from svl_qlog
 WHERE label like '%YOUR_LABEL%' and userid=100
 order by starttime desc;

-- Same as above, but summed by pid and label
select pid, label, MIN(starttime) as starttime_min, MAX(endtime) as endtime_max, SUM(elapsed)/1000 AS elapsed_msec, SUM(elapsed::DECIMAL)/1000000 as elapsed_sec, MAX(aborted) as aborted
from svl_qlog
WHERE label like '%query%' and userid=100
GROUP BY pid, label
order by starttime_min desc;

-- Query metrics summary
select sq.label, sq.starttime, sqms.query_cpu_time, sqms.query_blocks_read, sqms.query_execution_time,
sqms.query_cpu_usage_percent, sqms.query_temp_blocks_to_disk, sqms.segment_execution_time,
sqms.cpu_skew, sqms.io_skew, sqms.scan_row_count, sqms.join_row_count, sqms.return_row_count,
sqms.spectrum_scan_row_count, sqms.spectrum_scan_size_mb
FROM SVL_QUERY_METRICS_SUMMARY sqms JOIN svl_qlog sq ON sqms.query=sq.query
WHERE sq.label like '%YOUR_LABEL%' AND sq.userid=100
order by starttime desc;


 --Sum S3 traffic by query (if running Redshift Spectrum)
select sq.query, sq.label, SUM(s3_scanned_bytes)/1000000 AS s3_scanned_mb, SUM(s3query_returned_rows) as s3query_returned_rows, SUM(s3query_returned_bytes)/1000000 as s3query_returned_bytes_mb
from svl_s3query_summary sss INNER JOIN svl_qlog sq
ON sq.query=sss.query
GROUP BY sq.query, sq.label;
