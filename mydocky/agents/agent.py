import os
import autogen
from .registers import register_functions
from models import OpenAIModels # pylint: disable=import-error


class Agent:
    '''
    Initializing Agent
    '''

    def __init__(self):
        sys_prompt = open("mydocky/prompts/system.md", "r", encoding="utf-8")
        self.system_message = sys_prompt.read()

        self.user_proxy = autogen.UserProxyAgent(
            name = "user_proxy",
            human_input_mode = "NEVER",
            max_consecutive_auto_reply = 10,
            is_termination_msg = lambda msg: msg.get("content") is not None
            and "TERMINATE" in msg["content"],
            code_execution_config = False
        )

        self.configure_assistant()

        register_functions(self.assistant, self.user_proxy)

    def configure_assistant(self):
        '''
        configure Assistant
        '''
        self.assistant = autogen.AssistantAgent(
            name="assistant",
            system_message = self.system_message,
            llm_config = {
                "config_list": [
                    {
                        "model": OpenAIModels.GPT_35_TURBO,
                        "api_key": os.environ.get("OPENAI_API_KEY")
                    }
                ]
            },
            human_input_mode = "NEVER",
        )

    def start(self, question: str) -> str:
        '''
        inititate chat
        '''
        resp = self.user_proxy.initiate_chat(self.assistant, message=question,
                                             silent=False, clear_history=True)
        print(f"RESPONSE: {resp}")

        return resp.summary

if __name__ == "__main__":
    pass
