// Synthetic case study: import order-grain asset states produced by SQLite.
let
 Source=Csv.Document(File.Contents(pDataRoot & "/asset_status.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
 Headers=Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
 Typed=Table.TransformColumnTypes(Headers,{{"asset_id",type text},{"event_at",type datetime},{"city",type text},
 {"region",type text},{"motion_status",type text},{"idle_hours",type number},{"business_status",type text}})
in Typed
