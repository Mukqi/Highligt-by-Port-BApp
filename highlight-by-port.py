from burp import IBurpExtender, IProxyListener, IHttpRequestResponse
from burp import IInterceptedProxyMessage, ITab
from javax.swing import JPanel, JButton, JLabel, JTextField, JComboBox
from java.awt import GridBagLayout, GridBagConstraints

class BurpExtender(IBurpExtender, IProxyListener, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Highlight by Port")

        # Create the configuration tab
        self.config = Config(callbacks)

        # Add the tab to Burp Suite
        callbacks.addSuiteTab(self.config)

        callbacks.registerProxyListener(self)
        callbacks.issueAlert("Highlight by Port registered successfully!")
        print("Highlight by Port registered successfully!")

    def getTabCaption(self):
        return "Highlight by Port"
    
    def processProxyMessage(self, isRequest, message):
        message_listener_interface = message.getListenerInterface()
        port = message_listener_interface.split(":")[1]

        message_info = message.getMessageInfo()
        self.highlightRequest(message_info, port)


    def highlightRequest(self, request_response, port):
        # Highlight the request in the UI (example: mark it as 'green' for port 8080)
        for obj in self.config.config:
            if port in obj:
                request_response.setHighlight(obj[port])  # Green color (HEX)
                break

class Config(ITab):
    def __init__(self, callbacks):
        self.callbacks = callbacks
        self.tab_name = "Highlight by Port"
        
        # Create the main panel with a GridBagLayout
        self.panel = JPanel()
        self.panel.setLayout(GridBagLayout())
        self.constraints = GridBagConstraints()

        # Dropdown values
        self.dropdown_values = [
            "red", "orange", "yellow", "green", "cyan",
            "blue", "pink", "magenta", "gray", "none"
        ]

        self.config = []

        # Add 9 rows of textboxes with a dropdown next to each
        self.text_fields = []
        self.combo_boxes = []
        
        for row in range(9):
            label = JLabel("Port %d " % (row + 1))
            text_field = JTextField(10)
            combo_box = JComboBox(self.dropdown_values)
            
            # Add the label, textbox, and dropdown to the panel
            self.add_component(label, 0, row)
            self.add_component(text_field, 1, row)
            self.add_component(combo_box, 2, row)
            
            self.text_fields.append(text_field)
            self.combo_boxes.append(combo_box)

        # Save button
        self.save_button = JButton("Save Config")
        self.save_button.addActionListener(self.save_config)
        self.add_component(self.save_button, 0, 9, 3, 1)  # Span across all 3 columns

    def getTabCaption(self):
        return self.tab_name

    def getUiComponent(self):
        return self.panel

    def add_component(self, component, gridx, gridy, gridwidth=1, gridheight=1):
        """Helper function to add components to the layout with specified constraints."""
        self.constraints.gridx = gridx
        self.constraints.gridy = gridy
        self.constraints.gridwidth = gridwidth
        self.constraints.gridheight = gridheight
        self.constraints.anchor = GridBagConstraints.WEST
        self.panel.add(component, self.constraints)

    def save_config(self, event):
        # Iterate through the rows and capture the values of textboxes and dropdowns
        new_config = []
        for idx, (text_field, combo_box) in enumerate(zip(self.text_fields, self.combo_boxes)):
            text_value = text_field.getText()
            selected_color = combo_box.getSelectedItem()
            if text_value != None and text_value != "":
                obj = {}
                obj[text_value] = selected_color
                new_config.append(obj)
        self.config = new_config


