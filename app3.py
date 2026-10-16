import streamlit as st

class Node:
    """Represents an individual patient record stored dynamically  (in a Linked List.)"""
    def __init__(self, patient_id, name, age, condition, priority):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.condition = condition
        self.priority = priority  # 1 for Emergency, 2 for Normal
        self.next = None

# Persist the Linked List head across app reruns using Streamlit session state
if 'hospital_head' not in st.session_state:
    st.session_state.hospital_head = None

def register_patient(patient_id, name, age, condition, priority):
    new_node = Node(patient_id, name, age, condition, priority)
    if not st.session_state.hospital_head:
        st.session_state.hospital_head = new_node
    else:
        current = st.session_state.hospital_head
        while current.next:
            current = current.next
        current.next = new_node
    st.success(f"Patient {name} registered successfully!")

def treat_next_patient():
    if not st.session_state.hospital_head:
        st.warning("No patients in the queue to treat.")
        return

    target = None
    prev = None
    current = st.session_state.hospital_head
    
    # Priority Queue search: Find first emergency (priority == 1)
    while current:
        if current.priority == 1:
            target = current
            break
        prev = current
        current = current.next

    # If no emergency, use FIFO (pick the head)
    if not target:
        target = st.session_state.hospital_head
        st.session_state.hospital_head = st.session_state.hospital_head.next
    else:
        if prev:
            prev.next = target.next
        else:
            st.session_state.hospital_head = target.next

    priority_label = "🚨 EMERGENCY" if target.priority == 1 else "🟢 Normal"
    st.info(f"**Now Treating:** {target.name} (ID: `{target.patient_id}`) | Condition: *{target.condition}* | Status: **{priority_label}**")

# ================= PAGE CONFIG & STYLING =================
st.set_page_config(page_title="Hospital Emergency System", page_icon="🏥", layout="wide")

st.markdown("## 🏥 Hospital Emergency Management System")
#st.markdown("SY B.Tech Mini Project (Group C - MP 2): Dynamic Linked List & Priority Queue Implementation")
st.divider()

# ================= SIDEBAR INPUT FORM =================
st.sidebar.header("➕ Register New Patient")
with st.sidebar.form("patient_form", clear_on_submit=True):
    p_id = st.text_input("Patient ID", value="P001")
    p_name = st.text_input("Patient Name")
    p_age = st.number_input("Age", min_value=1, max_value=120, value=25)
    p_condition = st.text_input("Medical Condition / Issue")
    p_priority = st.selectbox(
        "Priority Level", 
        options=[1, 2], 
        format_func=lambda x: "🚨 1 - Emergency (High Priority)" if x == 1 else "🟢 2 - Normal (FIFO)"
    )
    
    submit_button = st.form_submit_button(label="Add Patient to System")
    if submit_button:
        if p_id and p_name:
            register_patient(p_id, p_name, p_age, p_condition, p_priority)
        else:
            st.error("Please enter both Patient ID and Name.")

# ================= MAIN DASHBOARD CONTROLS =================
if st.button("🩺 Treat Next Patient (Priority / FIFO Engine)", type="primary"):
    treat_next_patient()

st.divider()
st.subheader("📋 Current Hospital Patient Records (Dynamic Linked List)")

# Display Linked List contents as a table
current = st.session_state.hospital_head
if not current:
    st.info("The hospital queue is currently empty. Use the sidebar to register patients.")
else:
    patient_data = []
    while current:
        status_text = "🚨 EMERGENCY" if current.priority == 1 else "🟢 Normal"
        patient_data.append({
            "Patient ID": current.patient_id,
            "Name": current.name,
            "Age": current.age,
            "Condition": current.condition,
            "Priority Status": status_text
        })
        current = current.next
    
    # Render table nicely
    st.table(patient_data)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Clear records button placed at the bottom of the records chart
    if st.button("🗑️ Clear All Records", type="secondary"):
        st.session_state.hospital_head = None
        st.success("All records cleared successfully.")
        st.rerun()
        