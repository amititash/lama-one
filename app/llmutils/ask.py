# # For using WCS
import weaviate
import json
import os

client = weaviate.Client(
     url = "https://jira-full-vnbz4r56.weaviate.network",  # Replace with your endpoint
     auth_client_secret=weaviate.AuthApiKey(api_key="LFKi9eHc7blqtQ3VVw31d5Zl3PyLeOXhK8Bu"),  # Replace w/ your Weaviate instance API key
     additional_headers = {
         "X-OpenAI-Api-Key": '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'  # Replace with your inference API key
     }
 )


def get_scope(question, limit):
    
    generate_prompt = question

    print("prompt...", limit)

    n = int(limit)

    response = (
    client.query
    .get('Issue', ['summary', 'assignee'])
    .with_generate(
        grouped_task=generate_prompt,
        grouped_properties=['summary', 'issueType', 'status', 'assignee']  # available since client version 3.19.2
    )
    .with_near_text({
        'concepts': ['server side']
    })
    .with_limit(n)
    ).do()

    print(json.dumps(response, indent=2))

    return response

def get_summary(question, limit):

    generate_prompt = question
    print("prompt...", limit)
    n = int(limit)
    #For all the active on-going work, provide a summary of work in various stages (In progress, Review, Testing)
    generate_prompt = 'make a list of all the Issues into categories based on status.'

    response = (
    client.query
    .get('Issue', ['summary', 'assignee', 'status'])
    .with_generate(
        grouped_task=generate_prompt,
        grouped_properties=['status','summary']  # available since client version 3.19.2
    )
    .with_near_text({
        'concepts': ['server side']
    })
    .with_limit(n)
    ).do()

    print(json.dumps(response, indent=2))

    return response