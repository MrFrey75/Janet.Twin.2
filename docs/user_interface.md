# Janet Twin: Documentation — User Interface

**Requirements Document: PyQt Conversational GPT Client**

This document outlines the functional and non-functional requirements for a desktop application built with **PyQt**, serving as a conversational interface for a GPT model. The requirements are broken down into iterative steps suitable for progressive implementation.

---

## Step 1: Core UI Layout & Structure

The initial step is to establish the fundamental user interface layout.

- **Main Window**: Create a top-level `QMainWindow`.  
- **Split View**: The main window should have a horizontal split using a `QSplitter` widget.  
- **Left Pane (Collapsible)**: The left pane will be a collapsible sidebar. It should contain a vertical layout for the **tools list**.  
- **Right Pane (Main Area)**: The right pane will be the main application area. It will be a container for the chat interface.  

---

## Step 2: Core Chat Functionality

This step focuses on implementing the central chat interaction within the right pane.

- **Results Text Area**:  
  A `QTextEdit` (or similar) widget for displaying the chat conversation. This widget should be **non-editable** by the user.  

- **Input Text Area**:  
  A multi-line `QTextEdit` widget for user input.  

- **Input Handling**:  
  - Implement a key event handler to detect **Ctrl+Enter**.  
  - When Ctrl+Enter is pressed, clear the input area and submit the text to the model.  

- **Streaming Display**:  
  The model’s response should be displayed in the results area **word-by-word**. This will require a mechanism to handle and append new words as they are received.  

- **Loading Indicator**:  
  While the model is generating a response, display a simple **loading message or indicator** in a prominent location within the right pane. This message should disappear once the response is complete.  

---

## Step 3: Tool - Conversation History

This step adds the first tool to the left pane.

- **UI Component**:  
  Add a `QListWidget` (or similar) to the left pane, representing the **conversation history**.  

- **Saving Data**:  
  - Conversations should be saved automatically after each message exchange.  
  - Use the local file system or an **SQLite database** for persistence.  

- **Display**:  
  Each item in the list should display:  
  - A title for the conversation (e.g., the first few words of the first user message).  
  - The date.  

- **Functionality**:  
  When a user clicks on an item in the history, the **entire conversation** should be loaded and displayed in the main results text area.  

---

## Step 4: Tools - Logs & Raw Data

This step adds two more functional tools to the left pane.

- **Logs Tool**:  
  A simple text area that displays **application logs**. Logs should be a user-friendly record of actions and events.  

- **Raw Data Stream Tool**:  
  A non-editable text area that displays the **raw data stream** from the API (e.g., JSON responses) as it is received. This will be a **live-updating stream**.  

---

## Step 5: Tool - Settings

This step implements the application’s configuration tool.

- **UI Components**:  
  Create a form with input fields for various settings.  

- **Functionality**:  
  - Model parameters (e.g., temperature, max tokens).  
  - UI preferences (e.g., theme, font size).  
  - API key configuration.  

- **Saving Settings**:  
  Settings should be saved to a local configuration file (e.g., **INI**, **JSON**) so they persist between sessions.  

---

## Step 6: Non-Functional Requirements & Error Handling

This final step focuses on making the application robust and production-ready.

- **Cross-Platform Compatibility**:  
  The application must be functional on **Windows, macOS, and Linux**. The use of PyQt should facilitate this.  

- **Error Handling**:  
  - Wrap all API calls in `try...except` blocks (or similar).  
  - If an API call fails (e.g., lost internet connection), show an **informative message box or status bar message**. The application should not crash.  

- **Performance**:  
  - The application should launch quickly.  
  - The UI should remain **responsive**, even when loading large conversation histories. Asynchronous data loading may be required.  

---
