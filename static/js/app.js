// ============================================================
// AQUAGUARD AI
// CHATGPT STYLE FRONTEND
// ============================================================


// ============================================================
// AREA ANALYSIS
// ============================================================

async function analyzeArea() {

    const location =
        document.getElementById("location").value.trim();

    const issue =
        document.getElementById("issue").value;

    const result =
        document.getElementById("result");


    if (!location) {

        result.innerHTML = `
            <div class="error-message">
                Please enter a Chennai area.
            </div>
        `;

        return;
    }


    result.innerHTML = `
        <div class="loading-message">
            Checking area...
        </div>
    `;


    try {

        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    location: location,
                    issue: issue
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            result.innerHTML = `
                <div class="error-message">
                    ${escapeHTML(
                        data.error ||
                        "Something went wrong."
                    )}
                </div>
            `;

            return;
        }


        displayAreaResult(data);


    } catch (error) {

        result.innerHTML = `
            <div class="error-message">
                Unable to connect to AquaGuard AI.
            </div>
        `;

        console.error(error);
    }
}


// ============================================================
// DISPLAY AREA RESULT
// ============================================================

function displayAreaResult(data) {

    const result =
        document.getElementById("result");


    let html = "";


    // --------------------------------------------------------
    // LOCATION
    // --------------------------------------------------------

    if (data.location) {

        html += `

            <div class="result-section">

                <h2>Area Information</h2>

                <p>
                    <strong>Area:</strong>
                    ${escapeHTML(
                        data.location.locality ||
                        "Not available"
                    )}
                </p>

                <p>
                    <strong>Zone:</strong>
                    ${escapeHTML(
                        data.location.zone ||
                        "Not available"
                    )}
                </p>

                <p>
                    <strong>Ward:</strong>
                    ${escapeHTML(
                        String(
                            data.location.ward ||
                            "Not available"
                        )
                    )}
                </p>

            </div>

        `;
    }


    // --------------------------------------------------------
    // GROUNDWATER
    // --------------------------------------------------------

    if (data.groundwater) {

        if (
            data.groundwater.status ===
            "available"
        ) {

            const latest =
                data.groundwater.latest;


            html += `

                <div class="result-section">

                    <h2>
                        Groundwater Information
                    </h2>

                    <p>
                        <strong>
                            Latest reading:
                        </strong>

                        ${latest.depth_m} m
                    </p>

                    <p>
                        <strong>
                            Month:
                        </strong>

                        ${latest.month}
                        ${latest.year}
                    </p>

                    <p>
                        <strong>
                            Previous reading:
                        </strong>

                        ${
                            data.groundwater.previous
                            ? data.groundwater.previous.depth_m
                              + " m"
                            : "Not available"
                        }
                    </p>


                    ${
                        data.groundwater.change_m !== null
                        ?

                        `
                            <p>
                                <strong>
                                    Change:
                                </strong>

                                ${
                                    data.groundwater.change_m
                                } m
                            </p>
                        `

                        :

                        ""
                    }


                    <p class="data-warning">

                        ${
                            data.groundwater.warning ||
                            ""
                        }

                    </p>


                    <p class="data-source">

                        <strong>
                            Source:
                        </strong>

                        ${
                            data.groundwater.source ||
                            ""
                        }

                    </p>

                </div>

            `;

        } else {

            html += `

                <div class="result-section">

                    <h2>
                        Groundwater Information
                    </h2>

                    <p>
                        ${
                            data.groundwater.message ||
                            "No groundwater data available."
                        }
                    </p>

                </div>

            `;
        }
    }


    // --------------------------------------------------------
    // AUTHORITY
    // --------------------------------------------------------

    if (data.authority) {

        html += `

            <div class="result-section">

                <h2>
                    Responsible Authority
                </h2>

                <p>

                    <strong>
                        Authority:
                    </strong>

                    ${
                        data.authority.authority
                    }

                </p>


                <p>

                    <strong>
                        Reason:
                    </strong>

                    ${
                        data.authority.reason
                    }

                </p>


                <p>

                    <strong>
                        Complaint route:
                    </strong>

                    ${
                        data.authority.route
                    }

                </p>

            </div>

        `;
    }


    // --------------------------------------------------------
    // FOLLOW-UP QUESTIONS
    // --------------------------------------------------------

    html += `

        <div class="follow-up-section">

            <h2>
                What would you like to know next?
            </h2>


            <div class="follow-up-buttons">


                <button
                    onclick="askFollowUp(
                        'Why is groundwater decreasing in this area?'
                    )">

                    Why is groundwater decreasing?

                </button>


                <button
                    onclick="askFollowUp(
                        'What can people do to protect groundwater in this area?'
                    )">

                    What can I do?

                </button>


                <button
                    onclick="askFollowUp(
                        'Who is responsible for this water issue?'
                    )">

                    Who is responsible?

                </button>


                <button
                    onclick="askFollowUp(
                        'What government actions can help this area?'
                    )">

                    What can the government do?

                </button>


            </div>

        </div>

    `;


    result.innerHTML = html;
}


// ============================================================
// AQUAGUARD CHAT
// ============================================================

async function askAquaGuard() {

    const input =
        document.getElementById(
            "aquaguard-question"
        );


    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    const chat =
        document.getElementById(
            "aquaguard-chat"
        );


    // Add user question
    addUserMessage(
        chat,
        question
    );


    // Clear input
    input.value = "";


    autoResizeTextarea(input);


    // Scroll down
    scrollChatToBottom(chat);


    // Thinking
    const thinking =
        addAssistantMessage(
            chat,
            "AquaGuard is thinking..."
        );


    scrollChatToBottom(chat);


    try {

        const response =
            await fetch(
                "/api/rag-chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        const data =
            await response.json();


        thinking.remove();


        if (!response.ok) {

            addAssistantMessage(
                chat,
                escapeHTML(
                    data.error ||
                    "Something went wrong."
                )
            );

            scrollChatToBottom(chat);

            return;
        }


        addAssistantMessage(
            chat,
            formatAIResponse(
                data.answer
            )
        );


        scrollChatToBottom(chat);


    } catch (error) {

        thinking.remove();


        addAssistantMessage(
            chat,
            "Unable to connect to AquaGuard AI."
        );


        scrollChatToBottom(chat);


        console.error(error);
    }
}


// ============================================================
// GENERAL AI CHAT
// ============================================================

async function askGeneralQuestion() {

    const input =
        document.getElementById(
            "general-question"
        );


    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    const chat =
        document.getElementById(
            "general-chat"
        );


    // User question
    addUserMessage(
        chat,
        question
    );


    // Clear input
    input.value = "";


    autoResizeTextarea(input);


    scrollChatToBottom(chat);


    // Thinking
    const thinking =
        addAssistantMessage(
            chat,
            "Thinking..."
        );


    scrollChatToBottom(chat);


    try {

        const response =
            await fetch(
                "/api/general-chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        const data =
            await response.json();


        thinking.remove();


        if (!response.ok) {

            addAssistantMessage(
                chat,
                escapeHTML(
                    data.error ||
                    "Something went wrong."
                )
            );

            scrollChatToBottom(chat);

            return;
        }


        addAssistantMessage(
            chat,
            formatAIResponse(
                data.answer
            )
        );


        scrollChatToBottom(chat);


    } catch (error) {

        thinking.remove();


        addAssistantMessage(
            chat,
            "Unable to connect to the AI service."
        );


        scrollChatToBottom(chat);


        console.error(error);
    }
}


// ============================================================
// USER MESSAGE
// ============================================================

function addUserMessage(
    container,
    text
) {

    const message =
        document.createElement(
            "div"
        );


    message.className =
        "chat-message user-message";


    message.innerHTML = `

        <div class="message-content">

            ${escapeHTML(text)}

        </div>

    `;


    container.appendChild(
        message
    );


    return message;
}


// ============================================================
// ASSISTANT MESSAGE
// ============================================================

function addAssistantMessage(
    container,
    text
) {

    const message =
        document.createElement(
            "div"
        );


    message.className =
        "chat-message assistant-message";


    message.innerHTML = `

        <div class="message-content">

            ${text}

        </div>

    `;


    container.appendChild(
        message
    );


    return message;
}


// ============================================================
// FOLLOW-UP QUESTION
// ============================================================

async function askFollowUp(
    question
) {

    const result =
        document.getElementById(
            "result"
        );


    const oldChat =
        document.getElementById(
            "follow-up-chat"
        );


    if (oldChat) {
        oldChat.remove();
    }


    const chat =
        document.createElement(
            "div"
        );


    chat.id =
        "follow-up-chat";


    chat.className =
        "follow-up-chat";


    result.appendChild(
        chat
    );


    addUserMessage(
        chat,
        question
    );


    const thinking =
        addAssistantMessage(
            chat,
            "AquaGuard is thinking..."
        );


    try {

        const response =
            await fetch(
                "/api/follow-up",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        const data =
            await response.json();


        thinking.remove();


        if (!response.ok) {

            addAssistantMessage(
                chat,
                escapeHTML(
                    data.error ||
                    "Something went wrong."
                )
            );

            return;
        }


        addAssistantMessage(
            chat,
            formatAIResponse(
                data.answer
            )
        );


        scrollChatToBottom(chat);


    } catch (error) {

        thinking.remove();


        addAssistantMessage(
            chat,
            "Unable to connect to AquaGuard AI."
        );


        console.error(error);
    }
}


// ============================================================
// ENTER KEY
// ============================================================

function handleChatKey(
    event,
    type
) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();


        if (type === "aquaguard") {

            askAquaGuard();

        } else {

            askGeneralQuestion();

        }
    }
}


// ============================================================
// AUTO RESIZE TEXTAREA
// ============================================================

function autoResizeTextarea(
    textarea
) {

    textarea.style.height = "auto";

    textarea.style.height =
        Math.min(
            textarea.scrollHeight,
            130
        ) + "px";
}


// ============================================================
// TEXTAREA AUTO RESIZE EVENTS
// ============================================================

document.addEventListener(
    "input",
    function(event) {

        if (
            event.target.tagName ===
            "TEXTAREA"
        ) {

            autoResizeTextarea(
                event.target
            );
        }
    }
);


// ============================================================
// SCROLL CHAT
// ============================================================

function scrollChatToBottom(
    container
) {

    setTimeout(
        function() {

            container.scrollTo({

                top:
                    container.scrollHeight,

                behavior:
                    "smooth"

            });

        },
        50
    );
}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(text) {

    return String(text)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );
}


// ============================================================
// FORMAT AI RESPONSE
// ============================================================

function formatAIResponse(
    text
) {

    if (!text) {
        return "";
    }


    let html =
        escapeHTML(text);


    // Remove accidental backslash
    // before Markdown headings

    html =
        html.replace(
            /^\\(#{1,6})\s*/gm,
            "$1 "
        );


    // Code blocks

    html =
        html.replace(
            /```(?:[a-zA-Z0-9_+-]+)?\n?([\s\S]*?)```/g,
            "<pre><code>$1</code></pre>"
        );


    // Bold

    html =
        html.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // Italic

    html =
        html.replace(
            /(?<!\*)\*([^*\n]+)\*(?!\*)/g,
            "<em>$1</em>"
        );


    // Inline code

    html =
        html.replace(
            /`([^`]+)`/g,
            "<code>$1</code>"
        );


    // Headings

    html =
        html.replace(
            /^######\s+(.*)$/gm,
            "<h6>$1</h6>"
        );

    html =
        html.replace(
            /^#####\s+(.*)$/gm,
            "<h5>$1</h5>"
        );

    html =
        html.replace(
            /^####\s+(.*)$/gm,
            "<h4>$1</h4>"
        );

    html =
        html.replace(
            /^###\s+(.*)$/gm,
            "<h3>$1</h3>"
        );

    html =
        html.replace(
            /^##\s+(.*)$/gm,
            "<h2>$1</h2>"
        );

    html =
        html.replace(
            /^#\s+(.*)$/gm,
            "<h1>$1</h1>"
        );


    // Horizontal lines

    html =
        html.replace(
            /^\s*([-*_]){3,}\s*$/gm,
            "<hr>"
        );


    // Bullet list

    html =
        html.replace(
            /^\s*[-*+]\s+(.*)$/gm,
            "<li>$1</li>"
        );


    const lines =
        html.split("\n");


    let output = "";

    let insideList =
        false;


    lines.forEach(
        function(line) {

            const trimmed =
                line.trim();


            if (!trimmed) {

                if (insideList) {

                    output +=
                        "</ul>";

                    insideList =
                        false;
                }

                return;
            }


            // Heading

            if (
                /^<h[1-6]>/.test(
                    trimmed
                )
            ) {

                if (insideList) {

                    output +=
                        "</ul>";

                    insideList =
                        false;
                }


                output +=
                    trimmed;

                return;
            }


            // Horizontal line

            if (
                trimmed === "<hr>"
            ) {

                if (insideList) {

                    output +=
                        "</ul>";

                    insideList =
                        false;
                }


                output +=
                    "<hr>";

                return;
            }


            // List item

            if (
                trimmed.startsWith(
                    "<li>"
                )
            ) {

                if (!insideList) {

                    output +=
                        "<ul>";

                    insideList =
                        true;
                }


                output +=
                    trimmed;

                return;
            }


            // Normal paragraph

            if (insideList) {

                output +=
                    "</ul>";

                insideList =
                    false;
            }


            output +=
                `<p>${trimmed}</p>`;
        }
    );


    if (insideList) {

        output +=
            "</ul>";
    }


    return output;
}