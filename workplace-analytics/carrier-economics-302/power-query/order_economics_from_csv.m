// The synthetic CSV is a SQL model output, not the original reporting SQL.
let
 Source=Csv.Document(File.Contents(pDataRoot & "/order_economics.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
 Headers=Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
 Typed=Table.TransformColumnTypes(Headers,{{"order_id",type text},{"carrier",type text},{"lane",type text},
 {"revenue",Currency.Type},{"base_carrier_cost",Currency.Type},{"extra_pay",Currency.Type},
 {"total_carrier_cost",Currency.Type},{"gross_margin",Currency.Type},{"arrived_on_time",Int64.Type},
 {"confirmation_elapsed_hours",type number}})
in Typed
