import time

import streamlit as st

from reduce_expr import reduce_expression_step

st.title("Calculator")
st.markdown(
    """
<style>
.calculator-container {
    border: 2px solid #ddd;
    padding: 20px;
    background-color: #e0e0e0;
}

.expression-input {
    display: none;
}

.expression-output {
    background-color: #ffffcc; /* Yellowish display background */
    padding: 10px;
    border: 1px solid #ddd;
    color: black; 
    font-size: 18px; 
    text-align: right;
    height: 40px;
    margin-bottom: 10px;
}

.div.stTextInput {
    color: #333;
}

div.stButton > button:first-child {
    width: 100%; 
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    padding: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

if "expression" not in st.session_state:
    st.session_state["expression"] = ""
    st.session_state["expression_parts"] = []


if "evaluating" not in st.session_state:
    st.session_state["evaluating"] = False


def add_element(value: str):
    prev_element = (
        st.session_state["expression_parts"].pop()
        if st.session_state["expression_parts"]
        else ""
    )
    if value.isnumeric() and prev_element.isnumeric():
        st.session_state["expression_parts"].append(f"{prev_element}{value}")
    else:
        if prev_element != "":
            st.session_state["expression_parts"].append(prev_element)
        st.session_state["expression_parts"].append(str(value))
    st.session_state["expression"] = " ".join(st.session_state["expression_parts"])


def on_evaluate_click():
    st.session_state["evaluating"] = True


def reduce_expression():
    if len(st.session_state["expression_parts"]) <= 1:
        st.session_state["evaluating"] = False
    else:
        st.session_state["expression_parts"] = reduce_expression_step(
            st.session_state["expression_parts"]
        )
        st.session_state["expression"] = " ".join(st.session_state["expression_parts"])


def validate_expression() -> bool:
    try:
        eval(" ".join(st.session_state["expression_parts"]))
        return True
    except:
        return False


def main():
    with st.container():
        expression_output = st.empty()
        expression_output.markdown(
            f'<div class="expression-output">{st.session_state["expression"]}</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("1", on_click=add_element, args="1")
            st.button("4", on_click=add_element, args="4")
            st.button("7", on_click=add_element, args="7")
        with col2:
            st.button("2", on_click=add_element, args="2")
            st.button("5", on_click=add_element, args="5")
            st.button("8", on_click=add_element, args="8")
            st.button("0", on_click=add_element, args="0")
        with col3:
            st.button("3", on_click=add_element, args="3")
            st.button("6", on_click=add_element, args="6")
            st.button("9", on_click=add_element, args="9")

        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.button("(", on_click=add_element, args="(")
        with col5:
            st.button(")", on_click=add_element, args=")")
        with col6:
            st.button(
                "=", on_click=on_evaluate_click, disabled=not validate_expression()
            )

        st.write("")  # Add some space
        col8, col9, col10, col11 = st.columns(4)
        with col8:
            st.button("\+", on_click=add_element, args="+")
        with col9:
            st.button("\-", on_click=add_element, args="-")
        with col10:
            st.button("\*", on_click=add_element, args="*")
        with col11:
            st.button("/", on_click=add_element, args="/")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state["evaluating"]:
            reduce_expression()
        if st.session_state["evaluating"]:
            time.sleep(1)
            st.rerun()


if __name__ == "__main__":
    main()
