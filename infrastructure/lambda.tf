resource "aws_lambda_function" "executa_emr" {
  filename      = "lambda_function_payload.zip"
  function_name = var.lambda_function_name
  handler       = "lambda_function.handler"

  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  runtime = "python3.8"

}