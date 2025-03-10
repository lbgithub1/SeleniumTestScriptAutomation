import streamlit as st
import time
import pandas as pd
import altair as alt
import OpenAIChatVersion8OpenRouter
from IMPORTANTSeleniumTesting5AnmeldungWiWa import anmeldungWiWa
from HtmlPreprocesser import contextChunkingDS, htmlPreprocesser2, htmlPreprocesser2Multiplepages, contextChunkingDS02
from TestskriptVorlageInPromptUser1 import testSkriptVorlageVar1
from TestskriptvorlageInPromptFinal2 import testSkriptVorlageVar2

# Datei für das bereinigte HTML
datei3 = "CleanedWiWa3UI.html"
c = ""
testcasedescriptionUser = ""
errorMessageUserFromUI = ""
testCaseStepDescriptUserFromUI = ""
finalScript2AfterDeclination = ""
userURL2 = ""
# **Session State Initialisierung**
if "urlEntered" not in st.session_state:
    st.session_state.urlEntered = False
if "testScripts" not in st.session_state:
    st.session_state.testScripts = []
if "c" not in st.session_state:
    st.session_state.c = None
if "strWebsite" not in st.session_state:
    st.session_state.strWebsite = ""
if "showDeclineFields" not in st.session_state:
    st.session_state.showDeclineFields = False
if "showIntermediateSnippet" not in st.session_state:
    st.session_state.showIntermediateSnippet = False
if "testScriptGenerated2" not in st.session_state:
    st.session_state.testScriptGenerated2 = False
if "showDeclineFields2" not in st.session_state:
    st.session_state.showDeclineFields2 = False
if "helperForPlaceHolderExpanderAnalysis" not in st.session_state:
    st.session_state.helperForPlaceHolderExpanderAnalysis = False
if "finalScriptGeneratedFirstOne" not in st.session_state:
    st.session_state.finalScriptGeneratedFirstOne = ""
if "scriptPlacerholderVersion" not in st.session_state:
    st.session_state.scriptPlacerholderVersion = ""
if "finalScript" not in st.session_state:
    st.session_state.finalScript = ""
if "finalScript2" not in st.session_state:
    st.session_state.finalScript2 = ""
if "helperSkipMethod1" not in st.session_state:
    st.session_state.helperSkipMethod1 = False
if "helperSkipMethod2" not in st.session_state:
    st.session_state.helperSkipMethod2 = False
if "helperSkipMethod3" not in st.session_state:
    st.session_state.helperSkipMethod3 = False
if "helperSkipMethod4" not in st.session_state:
    st.session_state.helperSkipMethod4 = False
if "processFinishedTestScriptAccepted" not in st.session_state:
    st.session_state.processFinishedTestScriptAccepted = False
if "processFinishedTestScriptAccepted2" not in st.session_state:
    st.session_state.processFinishedTestScriptAccepted2 = False
if "testOver2WebPages" not in st.session_state:
    st.session_state.testOver2WebPages = False
if "inputTokenState" not in st.session_state:
    st.session_state.inputTokenState = 0
if "outputTokenState" not in st.session_state:
    st.session_state.outputTokenState = 0
if "estimatedCosts" not in st.session_state:
    st.session_state.estimatedCosts = 0

st.set_page_config(page_title="Selenium Test Script Generator", page_icon="", layout="centered")
st.title("Selenium Test Script Generator")
st.info(
    """
    🔹 The UI Will Guide You Through The Process. \n
    🔹 The Test Scripts Are Generated Based On Your Input. \n
    """
    )

#1. URL
userURL = st.text_input("Enter The URL You Would Like To Test:", key="url", placeholder="https://example.com")
#2. URL
st.session_state.testOver2WebPages = st.toggle("🔎 Test over several websites")




if st.session_state.testOver2WebPages:
    userURL2 = st.text_input("Enter The Second URL You Would Like To Test:", key="url2", placeholder="https://example2.com")

show_infographic = st.toggle("📖 How Does The Test Script Generator Work?")
if show_infographic:
    st.image("FunktionsweiseOverview.png", use_container_width=True)

if st.button("Save Website"):
    # Fall: Nur eine Webseite wird getestet
    if not st.session_state.testOver2WebPages:
        if userURL.strip():
            st.session_state.strWebsite = htmlPreprocesser2(anmeldungWiWa(userURL), datei3)
            st.session_state.c = contextChunkingDS02(st.session_state.strWebsite)
            st.success("✅ Website Saved Successfully ✅")
            time.sleep(0.5)
            st.session_state.urlEntered = True
        else:
            st.error("Please enter a valid URL.")
    # Fall: Zwei Webseiten werden getestet
    else:
        if userURL.strip() and userURL2.strip():
            print("URL 1\n")
            print(userURL)
            print("URL 2\n")
            print(userURL2)
            st.session_state.strWebsite = htmlPreprocesser2Multiplepages(anmeldungWiWa(userURL),
                                                                           anmeldungWiWa(userURL2),
                                                                           datei3)
            st.session_state.c = contextChunkingDS02(st.session_state.strWebsite)
            st.success("✅ Websites Saved Successfully ✅")
            time.sleep(0.5)
            st.session_state.urlEntered = True
        else:
            st.error("Please enter valid URLs for both websites.")

# 2. Testfallbeschreibung eingeben
if st.session_state.urlEntered:
    testcasedescriptionUser = st.text_area(
        "Enter Your Test Case Description:",
        key="description",
        placeholder="Goal of the test case:\nCheck...",
        height=300,
    )

    if st.button("Save Description And Start Generating") and not st.session_state.helperSkipMethod1:
        st.success("⏳ Test Script Generation Started ⏳")

        # **Generiere das erste Testskript**
        #finalScript ist eine Liste von OpenRouter bestehend aus zwei Testskripten
        result = OpenAIChatVersion8OpenRouter.domToGPTOpenRouter(
            st.session_state.c, st.session_state.description, testSkriptVorlageVar1, testSkriptVorlageVar2
        )
        st.session_state.finalScript = result["generated_scripts"]
        st.session_state.inputTokenState += result["token_counts"]["total_input_tokens"]
        st.session_state.outputTokenState += result["token_counts"]["total_output_tokens"]
        st.session_state.estimatedCosts += result["token_counts"]["estimated_cost"]

        # **Speichere das Skript in der Liste**
        if len(st.session_state.finalScript) == 2:
            st.session_state.testScripts.append(("Intermediate Script", st.session_state.finalScript[0]))  # Erstes Testskript
            print(st.session_state.finalScript[0])
            st.session_state.testScripts.append(("Final Script", st.session_state.finalScript[1]))  # Finales Testskript
            print(st.session_state.finalScript[1])
            st.session_state.finalScriptGeneratedFirstOne = st.session_state.finalScript[1]
            st.session_state.helperSkipMethod1 = True

    # **Anzeige aller generierten Testskripte**

if st.session_state.testScripts:  # Prüft, ob die Liste nicht leer ist
    st.subheader("Test Script (First Generation)")
    title, script = st.session_state.testScripts[-1]  # Letztes Element der Liste extrahieren
    with st.expander("", expanded=True):
        st.code(script, language="python")

# **Button-Gruppe für Akzeptieren/Ablehnen**
if st.session_state.testScripts:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Accept Test Script", key="acceptTestScript", icon="✅"):
            # st.success("You accepted the script!")
            st.session_state.showDeclineFields = False  # Verhindert UI-Sprünge
            st.session_state.processFinishedTestScriptAccepted = True

    with col2:
        if st.button("Decline Test Script", key="declineTestScript", icon="❌"):
            st.session_state.showDeclineFields = True
if st.session_state.showDeclineFields:
    st.warning("⚠️ You Have Rejected The Test Script Please Specify The Errors ⚠️️")
if st.session_state.processFinishedTestScriptAccepted:
    st.success("🏁 Process Finished Test Script Accepted 🏁")
    time.sleep(0.5)
    st.info(' Generating The Token Usage Analysis', icon="ℹ️")

    progress_bar = st.progress(0)
    for i in range(101):
        progress_bar.progress(i)
        time.sleep(0.01)

    if st.session_state.processFinishedTestScriptAccepted:
        with st.expander("📊 Token Usage & Cost Analysis", expanded=True):
            col1, col2 = st.columns([1, 1])

            with col1:

                st.metric(label="**Total Tokens:**",
                          value=f"{st.session_state.inputTokenState + st.session_state.outputTokenState:,.0f}".replace(',',
                                                                                                                       '.'))
                st.metric(label="**Total Input Tokens:**",
                          value=f"{st.session_state.inputTokenState:,.0f}".replace(',', '.'))
                st.metric(label="**Total Output Tokens:**",
                          value=f"{st.session_state.outputTokenState:,.0f}".replace(',', '.'))
                st.metric(label="**Estimated Cost:**", value=f"{st.session_state.estimatedCosts:,.2f} $".replace(',', '.'))
            with col2:
                total = st.session_state.inputTokenState + st.session_state.outputTokenState
                perc_input = (st.session_state.inputTokenState / total) * 100
                perc_output = (st.session_state.outputTokenState / total) * 100

                pie_data = pd.DataFrame([
                    {"Type": "Input", "Percent": perc_input},
                    {"Type": "Output", "Percent": perc_output}
                ])

                pie_chart = (
                    alt.Chart(pie_data)
                    .mark_arc(outerRadius=100, innerRadius=50)  # innerRadius=50 -> Donut
                    .encode(
                        theta=alt.Theta(field="Percent", type="quantitative"),
                        color=alt.Color(field="Type", type="nominal", legend=alt.Legend(title="Token Type")),
                        tooltip=[alt.Tooltip("Type:N", title="Token Type"),
                                 alt.Tooltip("Percent:Q", format=".2f", title="Percent")]
                    )
                    .properties(
                        title="Input vs Output (in %)",
                        width=300,
                        height=300
                    )
                )

                st.altair_chart(pie_chart, use_container_width=True)


# **Fehlermeldungseingabe nach Ablehnung**
if st.session_state.showDeclineFields:
    with st.container():
        errorMessageUserFromUI = st.text_area("Enter The Error Message From The Console:", key="error_message",
                                              placeholder="Paste the error message here...", height=150, )
        testCaseStepDescriptUserFromUI = st.text_area("Describe The Test Step Where The Error Occurred:",
                                                      key="test_step_description",
                                                      placeholder="Describe The Test Step In Detail...", height=150, )


        if st.button("Submit Improvements", key="submitFeedback"):
            st.success("⏳ Improvements Successfully Received - Second Iteration Started ⏳")
            st.session_state.showIntermediateSnippet = True
if st.session_state.showIntermediateSnippet and not st.session_state.helperSkipMethod2:
    # st.subheader("Try This One, While We Are Generating A New One")
    # title2, script2 = st.session_state.testScripts[0]
    # with st.expander(" ", expanded=True):
    #     st.code(script2, language="python")

    # **Erzeuge das zweite verbesserte Testskript**
    result2 = OpenAIChatVersion8OpenRouter.domToGPTOpenRouter02(
        st.session_state.c, st.session_state.description, testSkriptVorlageVar1, testSkriptVorlageVar2,
        errorMessageUserFromUI, testCaseStepDescriptUserFromUI, st.session_state.testScripts[-1][1]
    )
    st.session_state.finalScript2 = result2["generated_scripts"]
    st.session_state.inputTokenState += result2["token_counts"]["total_input_tokens"]
    st.session_state.outputTokenState += result2["token_counts"]["total_output_tokens"]
    st.session_state.estimatedCosts += result2["token_counts"]["estimated_cost"]

    st.session_state.testScripts.append(("Second Script (Improved)", st.session_state.finalScript2))
    st.session_state.testScriptGenerated2 = True
    st.session_state.helperSkipMethod2 = True

# **Finales verbessertes Testskript anzeigen**
# if st.session_state.testScriptGenerated2:
#     st.subheader("Improved Test Script (Second Generation):")
#     with st.expander(" ", expanded=True):
#         st.code(st.session_state.testScripts[-1][1], language="python")
#
#     col11, col22 = st.columns([1, 1])
#     with col11:
#         if st.button("Accept Improved Test Script", key="acceptTestScriptImproved", icon="✅"):
#             st.session_state.processFinishedTestScriptAccepted2 = True
#             st.session_state.showDeclineFields2 = False
#
#     with col22:
#         if st.button("Decline Improved Test Script", key="declineTestScriptImproved", icon="❌"):
#             st.session_state.showDeclineFields2 = True
#             # result3 = OpenAIChatVersion8OpenRouter.domToGPTOpenRouter03(
#             #         st.session_state.description, testSkriptVorlageVar1, st.session_state.finalScriptGeneratedFirstOne
#             #     )
#             # st.session_state.scriptPlacerholderVersion = result3["generated_scripts"]
#             # st.session_state.inputTokenState += result3["token_counts"]["total_input_tokens"]
#             # st.session_state.outputTokenState += result3["token_counts"]["total_output_tokens"]
#             # st.session_state.estimatedCosts += result3["token_counts"]["estimated_cost"]
#             st.session_state.showDeclineFields2 = True
#             time.sleep(2)
#             st.session_state.testScriptGenerated2 = False

if st.session_state.testScriptGenerated2:
    st.subheader("Improved Test Script (Second Generation):")
    with st.expander(" ", expanded=True):
        st.code(st.session_state.testScripts[-1][1], language="python")

    col11, col22 = st.columns([1, 1])
    with col11:
        if st.button("Accept Improved Test Script", key="acceptTestScriptImproved", icon="✅"):
            st.session_state.processFinishedTestScriptAccepted2 = True
            st.session_state.showDeclineFields = False  # Verhindert UI-Sprünge
            # st.session_state.processFinishedTestScriptAccepted = True
    with col22:
        if st.button("Decline Improved Test Script", key="declineTestScriptImproved", icon="❌"):
            # Setze den Zustand zurück, sodass das Feedback-Formular erneut angezeigt wird
            st.session_state.showDeclineFields = True
            st.session_state.testScriptGenerated2 = False
            st.session_state.showIntermediateSnippet = False
            st.session_state.helperSkipMethod2 = False
            st.success("Please re-enter your feedback for further improvements.")

if st.session_state.processFinishedTestScriptAccepted2:
    st.success("🏁 Process Finished Test Script Accepted 🏁")
    time.sleep(0.5)
    st.info(' Generating The Token Usage Analysis', icon="ℹ️")

    progress_bar = st.progress(0)
    for i in range(101):
        progress_bar.progress(i)
        time.sleep(0.01)

    if st.session_state.processFinishedTestScriptAccepted2:
        with st.expander("📊 Token Usage & Cost Analysis", expanded=True):
            col1, col2 = st.columns([1, 1])

            with col1:

                st.metric(label="**Total Tokens:**",
                          value=f"{st.session_state.inputTokenState + st.session_state.outputTokenState:,.0f}".replace(',',
                                                                                                                       '.'))
                st.metric(label="**Total Input Tokens:**",
                          value=f"{st.session_state.inputTokenState:,.0f}".replace(',', '.'))
                st.metric(label="**Total Output Tokens:**",
                          value=f"{st.session_state.outputTokenState:,.0f}".replace(',', '.'))
                st.metric(label="**Estimated Cost:**", value=f"{st.session_state.estimatedCosts:,.2f} $".replace(',', '.'))
            with col2:
                total = st.session_state.inputTokenState + st.session_state.outputTokenState
                perc_input = (st.session_state.inputTokenState / total) * 100
                perc_output = (st.session_state.outputTokenState / total) * 100

                pie_data = pd.DataFrame([
                    {"Type": "Input", "Percent": perc_input},
                    {"Type": "Output", "Percent": perc_output}
                ])

                pie_chart = (
                    alt.Chart(pie_data)
                    .mark_arc(outerRadius=100, innerRadius=50)  # innerRadius=50 -> Donut
                    .encode(
                        theta=alt.Theta(field="Percent", type="quantitative"),
                        color=alt.Color(field="Type", type="nominal", legend=alt.Legend(title="Token Type")),
                        tooltip=[alt.Tooltip("Type:N", title="Token Type"),
                                 alt.Tooltip("Percent:Q", format=".2f", title="Percent")]
                    )
                    .properties(
                        title="Input vs Output (in %)",
                        width=300,
                        height=300
                    )
                )

                st.altair_chart(pie_chart, use_container_width=True)