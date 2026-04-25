import base64
import os

def embed_logo(project_path):
    logo_path = os.path.join(project_path, 'logo.jpeg')
    app_path = os.path.join(project_path, 'app.js')
    
    if not os.path.exists(logo_path):
        print(f"Logo not found at {logo_path}")
        return

    with open(logo_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    
    with open(app_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Insert the logo string at the top
    logo_var = f"const LOGO_BASE64 = 'data:image/jpeg;base64,{encoded}';\n"
    
    # Logic to update all logo elements on DOMContentLoaded
    update_logic = """
    // Update all logo images in the DOM
    const updateLogos = () => {
        document.querySelectorAll('img[src="logo.jpeg"], img[alt*="Logo"]').forEach(img => {
            img.src = LOGO_BASE64;
        });
    };
    updateLogos();
"""

    # Find the line where DOMContentLoaded starts
    new_lines = []
    inserted_var = False
    inserted_logic = False
    
    for line in lines:
        if not inserted_var and 'import' not in line:
            new_lines.append(logo_var)
            inserted_var = True
        
        new_lines.append(line)
        
        if "document.addEventListener('DOMContentLoaded', async () => {" in line and not inserted_logic:
            new_lines.append(update_logic)
            inserted_logic = True

    with open(app_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Logo embedded successfully in app.js")

embed_logo('c:/Users/jdieg/c-31/c-31')
embed_logo('c:/Users/jdieg/U-8/u-8')
