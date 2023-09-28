import os

def format_action_payload():
  # substitute current tenant name in action code (dev or not dev), and write result
  template_file = "actions/set-claims-as-github-teams.js.tpl"
  output_file = "actions/set-claims-as-github-teams.js"

  with open(template_file, "r") as template:
      template_content = template.read()

  substituted_content = template_content.replace("$TENANT", os.environ.get("TENANT", ""))

  with open(output_file, "w") as output:
      output.write(substituted_content)

  # package the action js file as a string to include in API call to create/patch action
  output_string = ""
  with open(output_file, "r") as file:
      for line in file:
          # escape quotes and replace carriage returns with \n
          line = line.replace('"', '\\"').rstrip() + "\\n"
          output_string += line

  # substitute ENV values into request-body for action creation, and write result
  template_file = "request-body/create-action-body.json.tpl"
  output_file = "request-body/create-action-body.json"

  with open(template_file, "r") as template:
      template_content = template.read()

  substituted_content = template_content.replace("$ACTION_CODE", output_string)
  substituted_content = substituted_content.replace("$MANAGEMENT_API_CLIENT_ID", os.environ.get("MANAGEMENT_API_CLIENT_ID", ""))
  substituted_content = substituted_content.replace("$MANAGEMENT_API_CLIENT_SECRET", os.environ.get("MANAGEMENT_API_CLIENT_SECRET", ""))

  with open(output_file, "w") as output:
      output.write(substituted_content)
