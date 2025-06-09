document.addEventListener('DOMContentLoaded', () => {
    // 🔴 获取所有需要的DOM元素
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const sqlDisplay = document.getElementById('sql-display');
    const dataDisplay = document.getElementById('data-display');

    const API_URL = 'http://127.0.0.1:8000/api/v1/query';

    // ---- 事件监听 ----
    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // 阻止回车换行
            handleSendMessage();
        }
    });

    // ---- 函数定义 ----

    async function handleSendMessage() {
        const question = userInput.value.trim();
        if (!question) return;

        displayUserMessage(question);
        userInput.value = '';
        sendBtn.disabled = true;

        // 🔴 清空左侧信息栏并显示加载提示
        sqlDisplay.textContent = '正在生成SQL...';
        dataDisplay.textContent = '正在查询数据...';

        displayLoadingIndicator();

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            removeLoadingIndicator();

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || '网络请求失败');
            }

            const data = await response.json();
            // 🔴 调用新的函数来分别渲染不同部分
            renderResponsePanels(data);
            displayBotSummary(data.summary);

        } catch (error) {
            removeLoadingIndicator();
            displayErrorMessage(error.message);
            // 🔴 出错时清空左侧信息栏
            sqlDisplay.textContent = '查询出错';
            dataDisplay.textContent = '查询出错';
        } finally {
            sendBtn.disabled = false; // 重新启用按钮
            userInput.focus();
        }
    }

    /**
     * 🔴 新函数：将后端返回的数据渲染到左侧信息栏
     * @param {object} data
     */
    function renderResponsePanels(data) {
        // 渲染SQL语句
        if (data.sql_query && data.sql_query !== "未能提取SQL") {
            sqlDisplay.textContent = data.sql_query;
        } else {
            sqlDisplay.textContent = "未生成有效的SQL语句。";
        }

        // 渲染原始数据
        if (data.raw_data) {
            // 美化JSON输出
            dataDisplay.textContent = JSON.stringify(data.raw_data, null, 2);
        } else {
            dataDisplay.textContent = "没有返回原始数据。";
        }
    }

    function displayUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'flex justify-end mb-4';
        messageElement.innerHTML = `
            <div class="bg-blue-500 text-white p-3 rounded-lg shadow-sm max-w-lg break-words">
                ${message}
            </div>
        `;
        chatContainer.appendChild(messageElement);
        scrollToBottom();
    }

    /**
     * 🔴 新函数：只在聊天框里显示机器人的自然语言总结
     * @param {string} summary
     */
    function displayBotSummary(summary) {
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'flex justify-start mb-4';
        botMessageElement.innerHTML = `
            <div class="bg-white p-4 rounded-lg shadow-sm max-w-2xl border break-words">
                <p class="text-gray-800">${summary.replace(/\n/g, '<br>')}</p>
            </div>
        `;
        chatContainer.appendChild(botMessageElement);
        scrollToBottom();
    }


    function displayLoadingIndicator() {
        const loadingElement = document.createElement('div');
        loadingElement.id = 'loading-indicator';
        loadingElement.className = 'flex justify-start mb-4';
        loadingElement.innerHTML = `
            <div class="bg-gray-200 p-3 rounded-lg shadow-sm flex items-center space-x-2">
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
                <span class="text-gray-600">正在思考中...</span>
            </div>
        `;
        chatContainer.appendChild(loadingElement);
        scrollToBottom();
    }

    function removeLoadingIndicator() {
        const loadingElement = document.getElementById('loading-indicator');
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    function displayErrorMessage(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'flex justify-start mb-4';
        errorElement.innerHTML = `
            <div class="bg-red-100 text-red-700 p-3 rounded-lg shadow-sm max-w-lg border border-red-200 break-words">
                <strong>错误：</strong> ${message}
            </div>
        `;
        chatContainer.appendChild(errorElement);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
