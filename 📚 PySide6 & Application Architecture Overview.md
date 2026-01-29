# 📚 PySide6 & Application Architecture Overview

## 1. PySide6 Licensing: How it Works

When using PySide6 (Qt for Python), it is important to understand the license, especially in an engineering or commercial context.

- **The License:** PySide6 is primarily licensed under the **LGPL v3 (Lesser General Public License)**.

- **What this means for you (The Student/Developer):**
  
  - **Free to Use:** You can use PySide6 for free in open-source *and* proprietary (commercial) software.
  
  - **Dynamic Linking:** To keep your own code closed-source (proprietary), you must "dynamically link" to the library. In Python, simply `import PySide6` counts as dynamic linking. You do not need to share your own application's source code.
  
  - **No Modification:** You generally should not modify the PySide6 source code itself. If you do modify the library internals, you are obligated to share those changes.

- **Commercial Option:** There is a paid commercial license available if a company needs to modify Qt itself or cannot comply with LGPL requirements (e.g., for embedded devices where the user cannot replace the library).

---

## 2. GUI Hierarchy: How Layouts & Widgets Connect

In PySide (and Qt), the User Interface is built like a tree.

- **Widgets:** The actual elements you see (Buttons, Tables, Labels).

- **Layouts:** Invisible managers that calculate where Widgets sit and how they resize.

- **Containers:** Widgets that hold other layouts (like a `QGroupBox` or the main `QWidget` window).

### Visual Structure of the Factory App

The diagram below shows exactly how the code in `layout.py` builds the visual interface. Notice how we nest layouts inside groups, and groups inside other layouts.

![](/home/albert/.var/app/com.github.marktext.marktext/config/marktext/images/2025-12-19-10-07-14-image.png) 

## 3. Application Logic Flow

In an event-driven GUI like PySide, nothing happens until an event triggers it. In this application, the entire runtime logic originates from the **two buttons** on the right side of the interface.

This flow chart shows what happens when a student clicks the buttons.

- 

![](/home/albert/.var/app/com.github.marktext.marktext/config/marktext/images/2025-12-19-10-11-04-image.png)



### Key Takeaways for the Assignment

1. **Separation of Concerns:** The GUI (`layout.py`) doesn't know *how* to process an order. It just collects the data (Item & Quantity) and hands it off to the `processor.py`.

2. **The Trigger:** The entire chain of events starts with the `clicked.connect(...)` line in the Python code. If that connection isn't made, the button is just a decoration.

3. **The Critical Moment:** The diamond shape **"Is Stock Sufficient?"** occurs inside the Database Engine. If the answer is "No", Python catches the error. Your job is to ensure the flow moves to **Rollback**, not to **Step 2**.
