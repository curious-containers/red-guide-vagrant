cwlVersion: "v1.0"
class: "CommandLineTool"
baseCommand: "grepwrap"
doc: "Search for query terms in text files."

inputs:
  query_term:
    type: "string"
    inputBinding:
      position: 0
    doc: "Search for QUERY_TERM in TEXT_FILE."
  text_file:
    type: "File"
    inputBinding:
      position: 1
    doc: "TEXT_FILE containing plain text."
  after_context:
    type: "int?"
    inputBinding:
      prefix: "-A"
    doc: "Print NUM lines of trailing context after matching lines."
  before_context:
    type: "int?"
    inputBinding:
      prefix: "-B"
    doc: "Print NUM lines of leading context before matching lines."

outputs:
  out_file:
    type: "File"
    outputBinding:
      glob: "out.txt"
    doc: "Query results."
