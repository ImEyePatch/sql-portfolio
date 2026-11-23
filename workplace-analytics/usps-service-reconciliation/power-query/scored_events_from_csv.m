// Synthetic demo only. Create parameter pDataRoot pointing to a local folder.
let
  Source = Csv.Document(File.Contents(pDataRoot & "/scored_events.csv"),
    [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
  Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
  Typed = Table.TransformColumnTypes(Headers,{
    {"event_id",type text},{"load_id",type text},{"carrier",type text},{"lane",type text},
    {"event_type",type text},{"usps_on_time",Int64.Type},{"tms_on_time",Int64.Type},
    {"scored_before",Int64.Type},{"scored_after",Int64.Type},
    {"scored_if_pending_approved",Int64.Type},
    {"approved_exclusion",Int64.Type},{"pending_exclusion",Int64.Type},
    {"eligible_for_comparison",Int64.Type}})
in Typed
