

def local_inference(user_input='', local_llm=None, system_prompt=''):
    print("Running local inference, user_input: ", user_input)
    res = local_llm.create_chat_completion(
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return res['choices'][0]['message']['content']


def remote_inference(user_input='', system_prompt='', remote_llm_client=None):
    print("Running remote inference, user_input: ", user_input)
    res = remote_llm_client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7,
    )
    print(res)
    return res.choices[0].message.content
