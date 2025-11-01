import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import speech_recognition as sr

# Load dataset
df = pd.read_csv("cleaned_sales_data.csv")
sns.set(style="whitegrid")

# Page config
st.set_page_config(page_title="Voice-Controlled Dashboard", layout="centered")
st.title("🎙️ Voice-Controlled Sales Dashboard")

# Voice input function
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        st.success(f"✅ You said: '{command}'")
        return command.lower()
    except:
        st.error("❌ Could not understand your voice.")
        return ""

# Match voice to action
def interpret_command(command):
    if "product" in command:
        return "top_products"
    elif "category" in command:
        return "sales_by_category"
    elif "brand" in command:
        return "sales_by_brand"
    elif "employee" in command:
        return "sales_by_employee"
    else:
        return "unknown"

# Chart functions
def show_top_products():
    st.subheader("🏆 Top 10 Selling Products")
    top_products = df.groupby('item_name')['total'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_products.values, y=top_products.index, ax=ax, palette="Blues_r")
    st.pyplot(fig)

def show_sales_by_category():
    st.subheader("🗂️ Sales by Category")
    category_sales = df.groupby('category')['total'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=category_sales.values, y=category_sales.index, ax=ax, palette="coolwarm")
    st.pyplot(fig)

def show_sales_by_brand():
    st.subheader("🏷️ Top Brands by Sales")
    brand_sales = df.groupby('brand')['total'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=brand_sales.values, y=brand_sales.index, ax=ax, palette="mako")
    st.pyplot(fig)

def show_sales_by_employee():
    st.subheader("👩‍💼 Top Employees by Sales")
    employee_sales = df.groupby('employee_name')['total'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=employee_sales.values, y=employee_sales.index, ax=ax, palette="viridis")
    st.pyplot(fig)

# UI
if st.button("🎤 Start Voice Command"):
    command = get_voice_input()
    action = interpret_command(command)

    if action == "top_products":
        show_top_products()
    elif action == "sales_by_category":
        show_sales_by_category()
    elif action == "sales_by_brand":
        show_sales_by_brand()
    elif action == "sales_by_employee":
        show_sales_by_employee()
    else:
        st.warning("⚠️ Sorry, I didn't understand that command.")

st.markdown("---")
st.markdown("🗣️ Try saying: 'Show top products', 'Show sales by category', etc.")
