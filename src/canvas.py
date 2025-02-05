import streamlit.components.v1 as components

class Canvas:
    def __init__(self, width="100%", height=700):
        self.width = width
        self.height = height

    def functions(self):
        return """
        let mode = 'joint';
        let joints = [];
        let selectedJoints = [];
        let links = [];
        
        function setMode(newMode) {
            mode = newMode;
        }
        
        function addJoint(event) {
            if (mode !== 'joint') return;
            let container = document.getElementById("canvas-container");
            let rect = container.getBoundingClientRect();
            let x = event.clientX - rect.left;
            let y = event.clientY - rect.top;

            let joint = document.createElement("div");
            joint.classList.add("joint");
            joint.style.left = x + "px";
            joint.style.top = y + "px";
            joint.onclick = function(e) { selectJoint(e, x, y); };
            container.appendChild(joint);

            joints.push({x: x, y: y});
        }
        
        function selectJoint(event, x, y) {
            if (mode !== 'link') return;
            event.stopPropagation();
            selectedJoints.push({x, y});
            if (selectedJoints.length === 2) {
                links.push({joint1: selectedJoints[0], joint2: selectedJoints[1]});
                drawLink(selectedJoints[0], selectedJoints[1]);
                selectedJoints = [];
                sendDataToStreamlit();
            }
        }
        
        function drawLink(joint1, joint2) {
            let svg = document.getElementById("canvas-svg");
            let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", joint1.x+1.5);
            line.setAttribute("y1", joint1.y+1.5);
            line.setAttribute("x2", joint2.x+1.5);
            line.setAttribute("y2", joint2.y+1.5);
            line.setAttribute("stroke", "black");
            line.setAttribute("stroke-width", "3");
            svg.appendChild(line);
        }
        
        function sendDataToStreamlit() {
            const streamlitData = JSON.stringify({joints, links});
            Streamlit.setComponentValue(streamlitData);
        }
        """

    def render(self):
        function_script = self.functions()
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                #canvas-container {{
                    position: relative;
                    width: {self.width};
                    height: {self.height}px;
                    border: 1px solid black;
                    background-color: white;
                    margin-left: 10px;
                    max-width: 90vw;
                }}
                .joint {{
                    width: 10px;
                    height: 10px;
                    background-color: blue;
                    position: absolute;
                    border-radius: 50%;
                    cursor: pointer;
                }}
                svg {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                }}
            </style>
            <script>
                {function_script}
            </script>
        </head>
        <body>
            <button onclick="setMode('joint')">Add Joint</button>
            <button onclick="setMode('link')">Add Link</button>
            <div id="canvas-container" onclick="addJoint(event)">
                <svg id="canvas-svg"></svg>
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=self.height + 50)