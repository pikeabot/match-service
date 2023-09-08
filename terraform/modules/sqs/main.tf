resource "aws_sqs_queue" "example_match_queue_fifo" {
  name                       = "example-match-queue.fifo"
  delay_seconds              = 10
  visibility_timeout_seconds = 30
  max_message_size           = 2048
  message_retention_seconds  = 86400
  receive_wait_time_seconds  = 2
  fifo_queue                 = true
}

data "aws_iam_policy_document" "match-service-lambda-access" {
  statement {
    sid    = "MatchServiceLambdaAccess"
    effect = "Allow"

    principals {
      type        = "*"
      # TODO need to be able to make the identifiers a variable
      identifiers = ["*"]
    }

    actions   = ["*"]
    resources = [aws_sqs_queue.example_match_queue_fifo.arn]
  }
}

resource "aws_sqs_queue_policy" "match-servicelambda-access" {
  queue_url = aws_sqs_queue.example_match_queue_fifo.id
  policy    = data.aws_iam_policy_document.match-service-lambda-access.json
}
