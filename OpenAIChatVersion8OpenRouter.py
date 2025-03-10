import openai
from openai import OpenAI
import tiktoken
from HtmlPreprocesser import contextChunking, htmlPreprocesser2, htmlPreprocesser2Multiplepages, contextChunkingDS, contextChunkingDS02
from Prepocessor_2 import deleteEmptyTables, compactHtml
from IMPORTANTSeleniumTesting5AnmeldungWiWa import anmeldungWiWa, htmlCodeHelper
from TestskriptVorlageInPromptUser1 import testSkriptVorlageVar1
from TestskriptvorlageInPromptFinal2 import testSkriptVorlageVar2


#from GeneratedTestscriptsByGPT.YMTestfallbeschreibungWiWaAnmeldung import \
 #   testfallbeschreibungVar as tv


#import TestfallbeschreibungPrompt3WiWa1Produktsuche, TestfallbeschreibungPrompt4WiWa2Filterfunktion, \
  #  TestfallbeschreibungPrompt_FB
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

print(openai.__version__)

API_KEYkeyOpenAI = open("API_KEY", "r").read()
API_KEYkeyDeepSeek = open("APIKEYDEEPSEEK", "r").read().strip()
API_KEYkeyOpenRouter = open("API_KEY_OpenRouter", "r").read().strip()
# openai.api_key= API_KEYkey

clientOpenAI = OpenAI(api_key=API_KEYkeyOpenAI)
clientOpenDeepSeek = OpenAI(api_key=API_KEYkeyDeepSeek, base_url="https://api.deepseek.com/v1/")
clientOpenRouter = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEYkeyOpenRouter,
)
# clientOpenDeepSeek = OpenAI(api_key=API_KEYkeyDeepSeek, base_url="https://api.deepseek.com")


# ca. 210 Tokens
systemPrompt = SystemMessagePromptTemplate.from_template(
    """
You are a senior-level Python test automation engineer with extensive expertise in Selenium.
Your primary responsibility is to generate fully functional and accurate Selenium test scripts based on the given inputs. 
You will receive:
- A parse description detailing the test scenario and requirements.
- DOM content in structured chunks (Inclucded HTML).
- A prompt template that specifies coding standards, output format, and additional requirements.

Your tasks:
1. Strictly adhere to the prompt template and the instructions provided in the parse description.
2. Ensure all steps in the parse description are implemented correctly and completely.
3. You must meticulously follow the details in the user’s test scenario (e.g., the flow of actions, expected outcomes, environment).
4. You must provide the final script only, with no extra commentary.

Remember:
- Do not deviate from the instructions.
- Carefully analyze the test scenario, DOM content, and template to produce the highest quality script possible.
- Do not alter or summarize the instructions; follow them verbatim.
- Generate all your responses step by step.
"""
)

systemPromptFinal = SystemMessagePromptTemplate.from_template(
    """
You are a senior-level Python test automation engineer with extensive expertise in Selenium.
Your primary responsibility is to generate fully functional and accurate Selenium test scripts.
In the course you have already developed several fully functional Python Selenium test scripts, based on this, you must now create a final, perfect test script that strictly follows all instructions. 
You will receive:
- A prepared string containing all test scripts created by now
- A parse description detailing the test scenario and requirements.
- A prompt template that specifies coding standards, output format, and additional requirements.

Your tasks:
1. Strictly adhere to the prompt template and the instructions provided in the parse description.
2. Ensure all steps in the parse description are implemented correctly and completely.
3. You must meticulously follow the details in the user’s test scenario (e.g., the flow of actions, expected outcomes, environment).
4. You must provide the final Python Selenium script only, with no extra commentary.

Remember:
- Do not deviate from the instructions.
- Carefully analyze the given test scripts to produce the highest quality script possible.
- Do not alter or summarize the instructions; follow them verbatim.
- Generate all your responses step by step.
"""
)

# ca. 422 Tokens
userPrompt = HumanMessagePromptTemplate.from_template(
    """
**Instructions:**
1. **Test Requirements**: Implement Selenium tests strictly based on the following parse description:
   - Test Description: {parseDescriptionPrompt}
2. **Test Standards**:
   - Use the best possible locators - choose between ('By.LINK_TEXT' or 'By.XPATH').
   - 1st priority 'By.LINK_TEXT'.
   - 2nd priority 'By.XPATH' -> If you use Xpath, ALWAYS integrate the contains() function.
   - Avoid brittle locators that rely on dynamic attributes.
   - Ensure the script is optimized for readability and maintainability.
   - Always look out for ID attributes in the HTML code in order to adapt the Selenium selectors accordingly.
3. **Python Standards**:
   - Write clean, well-formatted Python code adhering to PEP-8 standards.
   - Include necessary Selenium imports.
   - Integrate comments to document the generated Selenium code.
   - Always use explicit waits via the time.sleep()-function - 4 seconds are appropriate.
   - Integrate an explicit wait via the time.sleep()-function, everytime the click()-function is executed in the script.
   - You need to ensure everytime that you search for the elements via the driver.find_element()-function.
   - Make sure that you use the click()-function to select the object in the script.
   - Integrate try-catch in the script.
   - You must use driver = webdriver.Chrome() to initialize the webdriver.
   - Integrate a short print()-Statement in the testscript, e.g. print('Test successful').
4. **DOM Chunks**:
    - The following DOM components are the foundation, based on the DOM chunks you have to create the Python Selenium test scripts.
    - Here are the DOM content:{domContent}
5. **Test script template**:
    - Make sure that you always include the first 5 lines in your test script in exactly the same way from the template, including the comments.
    - Use the test script template as a template to create your test script: {testScriptTemplate1}
    - Be aware, always integrate the anmeldungWiWaFuerSkript()-method, in the same order as testScriptTemplate1.
    - Always integrate the import of the method "from AnmeldungWiWaFuerTestskript import anmeldungWiWaFuerSkript".  
6. **Output Rules**:
   - Output **only** the test script. No additional explanations, comments, or irrelevant text.
   - Return an empty string ('') if the test description doesn't match any relevant DOM content.

**Additional Information:**
Provide a self-contained, runnable script that assumes the necessary Selenium setup (e.g., driver initialization).
Read all the Instructions again so that you pay attention to every detail.
Generate the script step by step.
"""
)

userPromptFinal = HumanMessagePromptTemplate.from_template(
    """
**Instructions:**
1. **Test Scope**: Use the provided Python Selenium test scripts:
   - {generatedTestscriptsListToString}
2. **Test Requirements**: Implement Selenium tests strictly based on the following parse description:
   - Test Description: {parseDescriptionPrompt}
3. **Test Standards**:
   - Use the best possible locators - choose between ('By.LINK_TEXT' or 'By.XPATH').
   - 1st priority 'By.LINK_TEXT'.
   - 2nd priority 'By.XPATH' -> If you use Xpath, ALWAYS integrate the contains() function.
   - Avoid brittle locators that rely on dynamic attributes.
   - Ensure the script is optimized for readability and maintainability.
   - Always look out for ID attributes in the HTML code in order to adapt the Selenium selectors accordingly.
4. **Python Standards**:
   - Write clean, well-formatted Python code adhering to PEP-8 standards.
   - Include necessary Selenium imports.
   - Integrate comments to document the generated Selenium code.
   - Always use explicit waits via the time.sleep()-function - 4 seconds are appropriate.
   - Integrate an explicit wait via the time.sleep()-function, everytime the click()-function is executed in the script.
   - You need to ensure everytime that you search for the elements via the driver.find_element()-function.
   - Make sure that you use the click()-function to select the object in the script.
   - Integrate try-catch in the script.
   - You must use driver = webdriver.Chrome() to initialize the webdriver.
   - Integrate a short print()-Statement in the testscript, e.g. print('Test successful').
5. **Test script template**:
   - Make sure that you always include the first 5 lines in your test script in exactly the same way from the template, including the comments.
   - Use the test script template as a template to create your test script: {testScriptTemplate2} 
   - Be aware, always integrate the anmeldungWiWaFuerSkript()-method, in the same order as testScriptTemplate2.
   - Always integrate the import of the method "from AnmeldungWiWaFuerTestskript import anmeldungWiWaFuerSkript".
6. **Output Rules**:
   - Output **only** the test script. No additional explanations, comments, or irrelevant text.
   - Return an empty string ('') if the test description doesn't match any relevant DOM content.

**Additional Information:**
Provide a self-contained, runnable script that assumes the necessary Selenium setup (e.g., driver initialization).
Read all the Instructions again so that you pay attention to every detail.
Generate the script step by step.
"""
)

userPrompt2UI = HumanMessagePromptTemplate.from_template(
    """
**Instructions:**
INFORMATION 1: Note in the previous creation of the test script, there was the following error message:{errorMessageFromUIPrompt}
INFORMATION 2: The user has entered a specification here:{teststepSpecificaFromUIPrompt}
INFORMATION 3: Here is the test script that you have already created, analyse it again, there must have been an error somewhere. If not, generate a new test script that fulfils all the requirements:{priorFinalTestScript}
Follow the steps in detail to generate a fully functional and correct Selenium test script that meets the requirements.
1. **Test Requirements**: Implement Selenium tests strictly based on the following parse description:
   - Test Description: {parseDescriptionPrompt}
2. **Test Standards**:
   - Use the best possible locators - choose between ('By.LINK_TEXT' or 'By.XPATH').
   - 1st priority 'By.LINK_TEXT'.
   - 2nd priority 'By.XPATH' -> If you use Xpath, ALWAYS integrate the contains() function.
   - Avoid brittle locators that rely on dynamic attributes.
   - Ensure the script is optimized for readability and maintainability.
   - Always look out for ID attributes in the HTML code in order to adapt the Selenium selectors accordingly.
3. **Python Standards**:
   - Write clean, well-formatted Python code adhering to PEP-8 standards.
   - Include necessary Selenium imports.
   - Integrate comments to document the generated Selenium code.
   - Always use explicit waits via the time.sleep()-function - 4 seconds are appropriate.
   - Integrate an explicit wait via the time.sleep()-function, everytime the click()-function is executed in the script.
   - You need to ensure everytime that you search for the elements via the driver.find_element()-function.
   - Make sure that you use the click()-function to select the object in the script.
   - Integrate try-catch in the script.
   - You must use driver = webdriver.Chrome() to initialize the webdriver.
   - Integrate a short print()-Statement in the testscript, e.g. print('Test successful').
4. **DOM Chunks**:
    - The following DOM components are the foundation, based on the DOM chunks you have to create the Python Selenium test scripts.
    - Here are the DOM content:{domContent}
5. **Test script template**:
    - Make sure that you always include the first 5 lines in your test script in exactly the same way from the template, including the comments.
    - Use the test script template as a template to create your test script: {testScriptTemplate1}
    - Be aware, always integrate the anmeldungWiWaFuerSkript()-method, in the same order as testScriptTemplate1.
    - Always integrate the import of the method "from AnmeldungWiWaFuerTestskript import anmeldungWiWaFuerSkript".  
6. **Output Rules**:
   - Output **only** the test script. No additional explanations, comments, or irrelevant text.
   - Return an empty string ('') if the test description doesn't match any relevant DOM content.

**Additional Information:**
Provide a self-contained, runnable script that assumes the necessary Selenium setup (e.g., driver initialization).
Read all the Instructions again so that you pay attention to every detail.
Generate the script step by step.
"""
)

userPrompt3UIPlaceholder = HumanMessagePromptTemplate.from_template(
    """
**Instructions:**
- Your task is to generate a Python Selenium test script, which is a placeholder variant. 
- So you should always use the XPATH selector from Selenium and then when the XPATH is to be integrated, you write the text = ‘PLACERHOLDERFORXPATH’. 
- The text is then replaced manually by the human in the next step, which is why this is a placeholder version.
Follow the steps in detail to generate a fully functional and correct Selenium test script that meets the requirements.
1. **Test Requirements**: Implement Selenium tests strictly based on the following parse description:
   - Test Description: {parseDescriptionPrompt}
2. **Test Standards**:
   - Always use the selector 'By.XPATH' and than insert 'PLACERHOLDERFORXPATH'
   - Ensure the script is optimized for readability and maintainability.
3. **Python Standards**:
   - Write clean, well-formatted Python code adhering to PEP-8 standards.
   - Include necessary Selenium imports.
   - Integrate comments to document the generated Selenium code.
   - Always use explicit waits via the time.sleep()-function - 4 seconds are appropriate.
   - Integrate an explicit wait via the time.sleep()-function, everytime the click()-function is executed in the script.
   - You need to ensure everytime that you search for the elements via the driver.find_element()-function.
   - Make sure that you use the click()-function to select the object in the script.
   - Integrate try-catch in the script.
   - You must use driver = webdriver.Chrome() to initialize the webdriver.
   - Integrate a short print()-Statement in the testscript, e.g. print('Test successful').
4. **Test script template**:
    - Make sure that you always include the first 5 lines in your test script in exactly the same way from the template, including the comments.
    - Use the test script template as a template to create your test script: {testScriptTemplate1Placeholder} - Placholder-Version.
    - Be aware, always integrate the anmeldungWiWaFuerSkript()-method, in the same order as testScriptTemplate1.
    - Always integrate the import of the method "from AnmeldungWiWaFuerTestskript import anmeldungWiWaFuerSkript".  
5. **Output Rules**:
   - Output only the test script. No additional explanations, comments, or irrelevant text.
   - Return an empty string ('') if the test description doesn't match any relevant DOM content.

**Reminder**:
- Only the By.XPATH selector is allowed in the test script.
- The path specification should contain ‘PLACERHOLDERFORXPATH’.
- You must follow these rules-
"""
)

systemStringCon = systemPrompt.format().content
systemStringFinalCon = systemPromptFinal.format().content
gptModels = ["o1-preview", "o1-preview-2024-09-12", "gpt-4o", "chatgpt-4o-latest"]
activeGptModel = 3

deepSeekModels = ["deepseek/deepseek-r1-distill-llama-70b", "deepseek/deepseek-r1"]
activeDSModel = 0


def domToGPT(domChunks, parseDescription, testScriptTemp1, testScriptTemp2):
    parsedResults2 = []  # Neu zum Vergleich

    for i, chunk in enumerate(domChunks, start=1):
        userStringCon = userPrompt.format(
            domContent=chunk,
            parseDescriptionPrompt=parseDescription,
            testScriptTemplate1=testScriptTemp1
        ).content

        # print(systemStringCon)
        # print(userStringCon)

        messages = [
            {"role": "system", "content": systemStringCon},
            {"role": "user", "content": userStringCon},
        ]

        # Hier nutzen wir jetzt client.chat.completions.create statt openai.ChatCompletion.create
        completion = clientOpenAI.chat.completions.create(
            model=gptModels[activeGptModel],
            messages=messages
        )

        aiResponse = completion.choices[0].message.content
        parsedResults2.append(aiResponse)

        # Fortschritt anzeigen
        print(f"Parsed batch: {i} of {len(domChunks)}")
        print(completion.choices[0].message.content)

    # Schritt2 Final Message
    generatedTestscripts = "\n\n".join(parsedResults2)

    userStringFinalCon = userPromptFinal.format(
        generatedTestscriptsListToString=generatedTestscripts,
        parseDescriptionPrompt=parseDescription,
        testScriptTemplate2=testScriptTemp2
    ).content

    finalMessages = [
        {"role": "system", "content": systemStringFinalCon},
        {"role": "user", "content": userStringFinalCon},
    ]

    finalCompletion = clientOpenAI.chat.completions.create(
        model=gptModels[activeGptModel],
        messages=finalMessages
    )

    # print(generatedTestscripts)
    finalResponse = finalCompletion.choices[0].message.content
    print("\n=== FINALES GENERIERTES TESTSKRIPT ===\n")
    print(finalResponse)

    return finalResponse.strip()


# clientOpenDeepSeek = OpenAI(api_key=API_KEYkeyDeepSeek, base_url="https://api.deepseek.com")
def domToGPTDeepSeek(domChunks, parseDescription, testScriptTemp1, testScriptTemp2):
    parsedResults2 = []  # Neu zum Vergleich
    # Liste verfügbarer Modelle abrufen
    print(f"Available models: {[m.id for m in clientOpenDeepSeek.models.list()]}")
    for i, chunk in enumerate(domChunks, start=1):
        userStringCon = userPrompt.format(
            domContent=chunk,
            parseDescriptionPrompt=parseDescription,
            testScriptTemplate1=testScriptTemp1

        ).content

        # print(systemStringCon)
        # print(userStringCon)

        messages = [
            {"role": "system", "content": systemStringCon},
            {"role": "user", "content": userStringCon},
        ]

        # Hier nutzen wir jetzt client.chat.completions.create statt openai.ChatCompletion.create
        completion = clientOpenDeepSeek.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            temperature=0.1,
            stream=False
        )

        aiResponse = completion.choices[0].message.content
        parsedResults2.append(aiResponse)

        # Fortschritt anzeigen
        print(f"Parsed batch: {i} of {len(domChunks)}")
        print(completion.choices[0].message.content)

    # Schritt2 Final Message
    generatedTestscripts = "\n\n".join(parsedResults2)

    userStringFinalCon = userPromptFinal.format(
        generatedTestscriptsListToString=generatedTestscripts,
        parseDescriptionPrompt=parseDescription,
        testScriptTemplate2=testScriptTemp2
    ).content

    finalMessages = [
        {"role": "system", "content": systemStringFinalCon},
        {"role": "user", "content": userStringFinalCon},
    ]

    finalCompletion = clientOpenDeepSeek.chat.completions.create(
        model="deepseek-reasoner",
        messages=finalMessages,
        temperature=0.1,
        stream=False
    )

    # print(generatedTestscripts)
    finalResponse = finalCompletion.choices[0].message.content
    print("\n=== FINALES GENERIERTES TESTSKRIPT ===\n")
    print(finalResponse)

    return finalResponse.strip()

def domToGPTOpenRouterBasisVersion(domChunks, parseDescription, testScriptTemp1, testScriptTemp2):
    parsedResults2 = []  # Neu zum Vergleich

    for i, chunk in enumerate(domChunks, start=1):
        userStringCon = userPrompt.format(
            domContent=chunk,
            parseDescriptionPrompt=parseDescription,
            testScriptTemplate1=testScriptTemp1
        ).content

        # print(systemStringCon)
        # print(userStringCon)

        messages = [
            {"role": "system", "content": systemStringCon},
            {"role": "user", "content": userStringCon},
        ]

        # Hier nutzen wir jetzt client.chat.completions.create statt openai.ChatCompletion.create
        completion = clientOpenRouter.chat.completions.create(
            model=deepSeekModels[activeDSModel],
            messages=messages
        )

        aiResponse = completion.choices[0].message.content
        parsedResults2.append(aiResponse)

        # Fortschritt anzeigen
        print(f"Parsed batch: {i} of {len(domChunks)}")
        print(completion.choices[0].message.content)

    # Schritt2 Final Message
    generatedTestscripts = "\n\n".join(parsedResults2)

    userStringFinalCon = userPromptFinal.format(
        generatedTestscriptsListToString=generatedTestscripts,
        parseDescriptionPrompt=parseDescription,
        testScriptTemplate2=testScriptTemp2
    ).content

    finalMessages = [
        {"role": "system", "content": systemStringFinalCon},
        {"role": "user", "content": userStringFinalCon},
    ]

    finalCompletion = clientOpenRouter.chat.completions.create(
        model=deepSeekModels[activeDSModel],
        messages=finalMessages
    )

    # print(generatedTestscripts)
    finalResponse = finalCompletion.choices[0].message.content
    print("\n=== FINALES GENERIERTES TESTSKRIPT ===\n")
    print(finalResponse)

    return finalResponse.strip()


def domToGPTOpenRouter(domChunks, parseDescription, testScriptTemp1, testScriptTemp2):
    parsedResults2 = []  # Neu zum Vergleich
    finalResponsesList = []
    parsedResults2.append("HierStehtInhalt")
    total_input_tokens = 0
    total_output_tokens = 0
    final_input_tokens = 0

    for i, chunk in enumerate(domChunks, start=1):
        userStringCon = userPrompt.format(
            domContent=chunk,
            parseDescriptionPrompt=parseDescription,
            testScriptTemplate1=testScriptTemp1
        ).content


        messages = [
            {"role": "system", "content": systemStringCon},
            {"role": "user", "content": userStringCon},
        ]

        input_tokens_current = count_tokens(userStringCon) + count_tokens(systemStringCon)  # Tokens für die aktuelle Iteration
        total_input_tokens += input_tokens_current  # Aufsummieren

        # Hier nutzen wir jetzt client.chat.completions.create statt openai.ChatCompletion.create
        completion = clientOpenRouter.chat.completions.create(
            model=deepSeekModels[activeDSModel],
            messages=messages
        )

        aiResponse = completion.choices[0].message.content
        parsedResults2.append(aiResponse)

        output_tokens_current = count_tokens(aiResponse)  # Tokens für Antwort
        total_output_tokens += output_tokens_current  # Aufsummieren

        # Fortschritt anzeigen
        print(f"Parsed batch: {i} of {len(domChunks)}")
        print(f"Tokens dieser Iteration: Input={input_tokens_current}, Output={output_tokens_current}")
        print(completion.choices[0].message.content)

    finalResponsesList.append(parsedResults2[-1])

    # Schritt2 Final Message
    generatedTestscripts = "\n\n".join(parsedResults2)
    # print("GeneratedTestscripts: \n\n" + generatedTestscripts)

    userStringFinalCon = userPromptFinal.format(
        generatedTestscriptsListToString=generatedTestscripts,
        parseDescriptionPrompt=parseDescription,
        testScriptTemplate2=testScriptTemp2
    ).content

    finalMessages = [
        {"role": "system", "content": systemStringFinalCon},
        {"role": "user", "content": userStringFinalCon},
    ]

    final_input_tokens = count_tokens(userStringFinalCon) + count_tokens(systemStringFinalCon)  # Tokens für den finalen Prompt
    total_input_tokens += final_input_tokens  # Aufsummieren

    finalCompletion = clientOpenRouter.chat.completions.create(
        model=deepSeekModels[activeDSModel],
        messages=finalMessages
    )



    # print(generatedTestscripts)
    finalResponse = finalCompletion.choices[0].message.content
    output_tokens_current = count_tokens(finalResponse)  # Tokens für Antwort
    total_output_tokens += output_tokens_current  # Aufsummieren
    print("\n=== FINALES GENERIERTES TESTSKRIPT ===\n")
    print(f"Tokens dieser Iteration: Input={final_input_tokens}, Output={output_tokens_current}")
    print(finalResponse)
    finalResponsesList.append(finalResponse.strip())

    estimated_cost = calculate_cost(total_input_tokens, total_output_tokens)

    for index, x in enumerate(finalResponsesList):
        print(f"{index}------------------------------------------\n\n")
        print(x)

    # helperDict = {}
    helperDict = {
        "generated_scripts": finalResponsesList,
        "token_counts": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost": estimated_cost
        }
    }
    print(f'Total Output Tokens:\t{helperDict["token_counts"]["total_output_tokens"]}')
    print(f'Total Input Tolkens:\t{helperDict["token_counts"]["total_input_tokens"]}')
    print(f'Estimated Cost:\t{helperDict["token_counts"]["estimated_cost"]}')
    # return finalResponsesList
    return {
        "generated_scripts": finalResponsesList,
        "token_counts": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost": estimated_cost
        }
    }

def domToGPTOpenRouter02(domChunks, parseDescription, testScriptTemp1, testScriptTemp2, errorMessageFromUI,
                         teststepSpecificaFromUI, priorFinalTestScriptFirstOne):
    parsedResults2 = []  # Neu zum Vergleich
    total_input_tokens = 0
    total_output_tokens = 0
    final_input_tokens = 0
    input_tokens_current = 0


    print("OpenRouter 02 Mit FehlerMessage und Spezifikationen\n\n Stehen hier")
    for i, chunk in enumerate(domChunks, start=1):
        userStringCon = userPrompt2UI.format(
            domContent=chunk,
            parseDescriptionPrompt=parseDescription,
            testScriptTemplate1=testScriptTemp1,
            errorMessageFromUIPrompt=errorMessageFromUI,
            teststepSpecificaFromUIPrompt=teststepSpecificaFromUI,
            priorFinalTestScript=priorFinalTestScriptFirstOne
        ).content



        # print(systemStringCon)
        # print(userStringCon)

        messages = [
            {"role": "system", "content": systemStringCon},
            {"role": "user", "content": userStringCon},
        ]

        input_tokens_current = count_tokens(userStringCon) + count_tokens(systemStringCon) # Tokens für die aktuelle Iteration
        total_input_tokens += input_tokens_current  # Aufsummieren

        # Hier nutzen wir jetzt client.chat.completions.create statt openai.ChatCompletion.create
        completion = clientOpenRouter.chat.completions.create(
            model=deepSeekModels[activeDSModel],
            messages=messages
        )

        aiResponse = completion.choices[0].message.content
        parsedResults2.append(aiResponse)

        output_tokens_current = count_tokens(aiResponse)  # Tokens für Antwort
        total_output_tokens += output_tokens_current  # Aufsummieren

        # Fortschritt anzeigen
        print(f"Parsed batch: {i} of {len(domChunks)}")
        print(completion.choices[0].message.content)

    # Schritt2 Final Message
    generatedTestscripts = "\n\n".join(parsedResults2)

    userStringFinalCon = userPromptFinal.format(
        generatedTestscriptsListToString=generatedTestscripts,
        parseDescriptionPrompt=parseDescription,
        testScriptTemplate2=testScriptTemp2
    ).content

    finalMessages = [
        {"role": "system", "content": systemStringFinalCon},
        {"role": "user", "content": userStringFinalCon},
    ]

    final_input_tokens = count_tokens(userStringFinalCon) + count_tokens(systemStringFinalCon) # Tokens für den finalen Prompt
    total_input_tokens += final_input_tokens  # Aufsummieren

    finalCompletion = clientOpenRouter.chat.completions.create(
        model=deepSeekModels[activeDSModel],
        messages=finalMessages
    )

    # print(generatedTestscripts)
    finalResponse = finalCompletion.choices[0].message.content
    output_tokens_current = count_tokens(finalResponse)  # Tokens für Antwort
    total_output_tokens += output_tokens_current  # Aufsummieren
    print("\n=== FINALES GENERIERTES TESTSKRIPT ===\n")
    print(finalResponse)
    estimated_cost = calculate_cost(total_input_tokens, total_output_tokens)

    # return finalResponse.strip()

    helperDict = {
        "generated_scripts": finalResponse,
        "token_counts": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost": estimated_cost
        }
    }

    print(f'Total Output Tokens:\t{helperDict["token_counts"]["total_output_tokens"]}')
    print(f'Total Input Tolkens:\t{helperDict["token_counts"]["total_input_tokens"]}')
    print(f'Estimated Cost:\t{helperDict["token_counts"]["estimated_cost"]}')
    # return finalResponsesList
    return {
        "generated_scripts": finalResponse,
        "token_counts": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost": estimated_cost
        }
    }

def domToGPTOpenRouter03(parseDescription, testScriptTemp1, priorFinalTestScriptFirstOne):
    print("PLACEHOLDER\n\nMethode wird gestartet")
    total_input_tokens = 0
    total_output_tokens = 0
    final_input_tokens = 0
    input_tokens_current = 0
    userStringCon = userPrompt3UIPlaceholder.format(
        parseDescriptionPrompt=parseDescription,
        testScriptTemplate1Placeholder=testScriptTemp1,
        priorFinalTestScript=priorFinalTestScriptFirstOne
    ).content

    # print(systemStringCon)
    # print(userStringCon)

    messages = [
        {"role": "system", "content": systemStringCon},
        {"role": "user", "content": userStringCon},
    ]

    input_tokens_current = count_tokens(userStringCon) + count_tokens(systemStringCon)  # Tokens für die aktuelle Iteration
    total_input_tokens += input_tokens_current  # Aufsummieren

    # Hier nutzen wir jetzt client.chat.completions.create statt openai.ChatCompletion.create
    completion = clientOpenRouter.chat.completions.create(
        model=deepSeekModels[activeDSModel],
        messages=messages
    )

    aiResponse = completion.choices[0].message.content

    output_tokens_current = count_tokens(aiResponse)  # Tokens für Antwort
    total_output_tokens += output_tokens_current  # Aufsummieren

    print("\n=== FINALES PLACEHOLDER TESTSKRIPT ===\n")
    print(aiResponse)

    estimated_cost = calculate_cost(total_input_tokens, total_output_tokens)

    # return aiResponse.strip()

    helperDict = {
        "generated_scripts": aiResponse,
        "token_counts": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost": estimated_cost
        }
    }
    print(f'Total Output Tokens:\t{helperDict["token_counts"]["total_output_tokens"]}')
    print(f'Total Input Tolkens:\t{helperDict["token_counts"]["total_input_tokens"]}')
    print(f'Estimated Cost:\t{helperDict["token_counts"]["estimated_cost"]}')
    # return finalResponsesList
    return {
        "generated_scripts": aiResponse,
        "token_counts": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost": estimated_cost
        }
    }

def count_tokens(text, model="gpt-4o"):
    """ Berechnet die Anzahl der Tokens im gegebenen Text basierend auf dem Modell. """
    encoder = tiktoken.encoding_for_model(model)
    return len(encoder.encode(text))

def calculate_cost(input_tokens, output_tokens, model="gpt-4o"):
    """ Berechnet die geschätzten Kosten für die Token-Nutzung. """
    costPerMillionInputDS = 0.55
    costPerMillionOutputDS = 2.19
    total_cost = (((input_tokens) / 1_000_000) * costPerMillionInputDS) + (((output_tokens) / 1_000_000) * costPerMillionOutputDS)
    return round(total_cost, 5)


if __name__ == "__main__":
    website = "https://eccoforst.de/"
    datei = "CleanedPageEccoForest.html"
    website1 = "https://www.jetbrains.com/de-de/idea/"
    datei1 = "inteliJCleaned.html"

    # parseDescription3 = TestfallbeschreibungPrompt2.testfallbeschreibungVar
    parseDescription4 = TestfallbeschreibungPrompt3WiWa1Produktsuche.testfallbeschreibungVar
    parseDescription5 = TestfallbeschreibungPrompt4WiWa2Filterfunktion.testfallbeschreibungVar
    parseDescription6 = TestfallbeschreibungPrompt_FB.testfallbeschreibungVar
    parseDescriptionAnmeldung = tv
    datei2 = "CleanedWaWi.html"
    urli = "https://wiwa.uni-trier.de/produkte/produkte"
    datei3 = "CleanedWiWa2.html"
    urli3 = "https://wiwa.uni-trier.de/login/logout"
    datei4 = "FacebookAnmeldung.html"
    urli4 = "https://www.facebook.com/r.php?entry_point=login"
    urlLogin = "https://wiwa.uni-trier.de"
    datei5 = "WiWaAnmeldung.html"
    datei6 = "WiWaReports.html"
    urli6 = "https://wiwa.uni-trier.de/index.php/reports/reports"
    datei7 = "WiWaAllgSuche.html"
    urli7 = "https://wiwa.uni-trier.de"
    urli81 = "https://wiwa.uni-trier.de"
    urli82 = "https://wiwa.uni-trier.de/index.php/home/loop"
    datei8 = "WiWaAllgSuchePs"
    urli91 = "https://wiwa.uni-trier.de"
    urli92 = "https://wiwa.uni-trier.de/admin/adminitems/hersteller/0"
    datei9 = "WiWaHerstellerAnlegen.html"
    datei10 = "WiWaHerstellerAnlegen.html"
    urli10 = "https://wiwa.uni-trier.de//produkte/produktlinie/15/1/0"

    #######strWebsite = htmlPreprocesser2(anmeldungWiWa(urli), datei3)
    # strWebsite = htmlPreprocesser2(htmlCodeHelper(urli3), datei3)
    # strWebsite = htmlPreprocesser2Multiplepages(anmeldungWiWa(urli91), anmeldungWiWa(urli92), detei9)
    # strWebsite = htmlPreprocesser(urlLogin, datei5)
    # c = contextChunking(strWebsite)
    # c = contextChunkingDS(strWebsite)
    ######c = contextChunkingDS02(strWebsite)
    # domToGPT(c, tvPÜEK, testSkriptVorlageVar1, testSkriptVorlageVar2)
    # domToGPTOpenRouter(c, tvPÜEK, testSkriptVorlageVar1, testSkriptVorlageVar2)
    ###### domToGPTOpenRouter(c, TLA, testSkriptVorlageVar1, testSkriptVorlageVar2)
    # domToGPTDeepSeek(c, tv, testSkriptVorlageVar1, testSkriptVorlageVar2)
    # To Do bei neuem Testfall
    # 1. Testfallbeschreibung ändern
    # 2. Datei erstellen .html
    # 3. URL anpassen
    # 4. domToGPT -> Testfallbeschreibung auch der Methode übergeben
    x = calculate_cost(111045 ,2910)
    print(x)


def runProgramm(link, datei, beschreibung):
    print("runProgramm wird ausgeführt")
    if (not link or not datei or not beschreibung):
        return "Bitte alles ausfüllen"
    with open("outputHelp.txt", "w") as file:
        file.write("Text wird generiert. Bitte Warten")
    strWebsite = htmlPreprocesser2(anmeldungWiWa(link), datei)
    c = contextChunking(strWebsite)
    returnText = domToGPT(c, beschreibung, testSkriptVorlageVar1, testSkriptVorlageVar2)
    # returnText = domToGPT(c, beschreibung)
    print(returnText)
    with open("outputHelp.txt", "w") as file:
        file.write(returnText)
    return returnText
    # return "Hier wird Text der den Code enthält übergeben" + link + " \n" + datei + "\n" + "Noch überprüfen dass link, Beschreibung und Datei nicht leer sind!!!"
