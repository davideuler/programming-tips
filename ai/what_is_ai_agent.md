
# What is AI Agent? 

## Agents are models using tools in a loop: LLM in the loop

LLM in the loop (From ai.engineer & Claude)
![image](https://github.com/user-attachments/assets/3a9a7061-af2e-4fa1-b2e1-95399df4e68b)


## An Example -  An Agent to Get all the links from Hacker News.

![image](https://github.com/user-attachments/assets/67e2044b-9dbf-4ff1-9af7-ac2cf9e404fe)

![image](https://github.com/user-attachments/assets/0821b862-6d7a-4337-82ea-1a96526d42a0)

https://www.willowtreeapps.com/craft/building-ai-agents-with-plan-and-execute

To do this, we need to:
* Send the planning system prompt to the LLM to create a plan and save those tasks as a list.
* For every task in that list:
* Keep track of the task given to the agent.
* Pull in the task prompt with the history.
* Call the LLM to choose a tool based on the given task and return as JSON.
* Update our memory with the LLM response.
* Match the tool called by the LLM to one of the tools available.
* Run the function called.
* Start the next task.

``` Python
## Plan and Execute
    def run(self, prompt: str):
        ## Planning
        planning = self.openai_call(prompt, self.planning_system_prompt)
        self.planned_actions = planning.split("\n")

        ## Task Execution
        for task in self.planned_actions:
            print(f"\n\nExecuting task: {task}")
            self.memory_tasks.append(task)
            self.update_system_prompt()
            task_call = self.openai_call(task, self.system_prompt, True)
            self.memory_responses.append(task_call)

            try:
                task_call_json = json.loads(task_call)
            except json.JSONDecodeError as e:
                print(f"Error decoding task call: {e}")
                continue

            tool = task_call_json.get("tool")
            variables = task_call_json.get("variables", [])

            if tool == "open_chrome":
                self.open_chrome()
                self.memory_responses.append("open_chrome=completed.")

            elif tool == "get_https_links":
                self.links = self.get_https_links(self.url)
                self.memory_responses.append(f"get_https_links=completed. variable urls = {self.links}")

            elif tool == "navigate_to_hackernews" :
                query = variables[0].get("variable_value", "")
                self.navigate_to_hackernews(query)
                self.memory_responses.append(f"navigate_to_hackernews=completed. variable query = {query}")



if __name__ == "__main__":
    agent = Agent()

    while True:
        prompt = input("Please enter a prompt (or type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        agent.run(prompt)
```
