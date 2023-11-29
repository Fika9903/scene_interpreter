import openai
import json


class QuestionAnswerer:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def answer_question(self, question: str, scene: dict) -> str:
        """
        Answer a question based on the scene context using GPT-3.

        :param question: The question in string format.
        :param scene: The scene description in dictionary format.
        :return: The answer to the question in string format.
        """
        try:
            scene_context = json.dumps(scene)
            print(scene_context)
            # Set up OpenAI API call
            openai.api_key = self.api_key
            # response = openai.Completion.create(
            #     model="gpt-3.5-turbo",
            #     prompt=input_text
            # )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "Your job is to examine a Scene description given in JSON format and answer a question given regarding the scene."},
                        {"role": "user", "content": scene_context},
                        {"role": "user", "content": question}
                    ]
                )
            answer = response['choices'][0]['message']['content'].strip()
            print(answer)
        except Exception as e:
            raise Exception("Failed to generate an answer using GPT-3. Please check the question and scene.") from e
        return answer
