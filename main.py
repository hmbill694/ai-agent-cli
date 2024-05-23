import typer
import chat_service
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os

app = typer.Typer()

@app.command()


def prompt(prompt: str):
    llm = ChatOpenAI(
        model = "phi3",
        base_url = "http://localhost:11434/v1")

    general_agent = Agent(role = "Poet",
                        goal = """You seek to write the best hikus possible.""",
                        backstory = """You come from a long line of famous poets. 
                        It is your passion as well. It is your lifes ambition to one day be known as the best in the field.""",
                        allow_delegation = False,
                        verbose = True,
                        llm = llm)

    writer = Task (description=f"Create a haiku using this prompt: {prompt}",
                expected_output="""3 haikus representing the essence of the provided prompt. PRESENT ONLY THE HAIKUS""",
                agent = general_agent)

    picker = Task (description=f"Pick the best of the 3 provided haikus. The hiku selected should capture the essence of {prompt}",
                expected_output="""A technically perfect haiku that captures the esscense of the subject. PRESENT ONLY THE HAIKU""",
                agent = general_agent)

    editor = Task (description="""Edit the provided poem and make any changes to ensure it is a adheres to the 5, 7, 5 rule. """,
                expected_output="""The final output of your edits. PRESENT ONLY THE HAIKU""",
                agent = general_agent)

    crew = Crew(
                agents=[general_agent],
                tasks=[writer, picker, editor],
                verbose=2
            )

    print("Starting the crew")

    result = crew.kickoff()

    print("--Here's what we came up with--\n\n")

    print(result)


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "NA"
    app()