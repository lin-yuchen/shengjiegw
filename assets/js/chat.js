// 聊天式 AI 交互功能

(function initChatWidget(){
    var chatWindow = document.getElementById('chatWindow');
    var chatInput = document.getElementById('chatInput');
    var chatSend = document.getElementById('chatSend');

    if (!chatWindow || !chatInput || !chatSend) return;

    function appendMessage(text, who){
        var m = document.createElement('div');
        m.className = 'message ' + (who === 'user' ? 'user' : 'ai');
        m.innerHTML = '<div class="text">'+ escapeHtml(text) +'</div>' + (who === 'ai' ? '<div class="meta">AI 助手</div>' : '');
        chatWindow.appendChild(m);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function escapeHtml(str){ 
        return String(str)
            .replace(/&/g,'&amp;')
            .replace(/</g,'&lt;')
            .replace(/>/g,'&gt;')
            .replace(/"/g,'&quot;')
            .replace(/'/g,'&#039;');
    }

    function simulateAIReply(userText){
        return new Promise(function(resolve){
            setTimeout(function(){
                var lower = userText.toLowerCase();
                if (lower.indexOf('价格') !== -1 || lower.indexOf('费用') !== -1) {
                    resolve('关于价格，我们提供按项目与按服务两种计费方式，建议先沟通需求以便给出报价。');
                }
                else if (lower.indexOf('合作') !== -1) {
                    resolve('我们欢迎合作。请提供贵司规模与期望服务内容，我方将安排客户经理联系。');
                }
                else if (lower.indexOf('发票') !== -1) {
                    resolve('可开具正规发票/收据，具体根据服务与地域政策决定，请告诉我们具体需求。');
                }
                else if (lower.indexOf('服务') !== -1) {
                    resolve('我们提供香港劳务外包、人力资源、宅配城配、打板及跨境运输服务。您想了解哪一项？');
                }
                else if (lower.indexOf('联系') !== -1 || lower.indexOf('电话') !== -1) {
                    resolve('您可以拨打我们的客服热线：+852 95790010，或发送邮件至 postmaster@r-quick.cn。');
                }
                else if (lower.indexOf('地址') !== -1) {
                    resolve('我们的公司地址在香港xxxxxx。具体位置可以查看页面底部的地图。');
                }
                else if (lower.indexOf('时间') !== -1 || lower.indexOf('办公') !== -1) {
                    resolve('办公时间：周一至周五 9:00 - 18:00，周六 9:00 - 14:00，周日及公众假期休息。');
                }
                else {
                    resolve('感谢提问！我们已收到您的问题："' + userText + '"。如需更详细资料，请留下联系方式或稍后联系我们的客服。');
                }
            }, 900 + Math.random()*800);
        });
    }

    // 如果希望集成真实 AI（OpenAI/OpenAI-compatible），请替换 simulateAIReply，示例：
    // function getAIReplyFromServer(prompt){
    //   return fetch('/api/ai', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({prompt})})
    //     .then(r=>r.json()).then(j=>j.reply);
    // }

    function sendCurrent(){
        var txt = chatInput.value && chatInput.value.trim();
        if (!txt) return;
        
        appendMessage(txt, 'user');
        chatInput.value = '';
        
        // 显示 loading 气泡
        var loading = document.createElement('div');
        loading.className = 'message ai';
        loading.innerHTML = '<div class="text">正在生成回复…</div>';
        chatWindow.appendChild(loading);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // 调用模拟 AI（或真实 API）
        simulateAIReply(txt).then(function(reply){
            // 替换 loading
            chatWindow.removeChild(loading);
            appendMessage(reply, 'ai');
        }).catch(function(err){
            chatWindow.removeChild(loading);
            appendMessage('抱歉，AI 回复失败，请稍后再试。', 'ai');
            console.error('AI error', err);
        });
    }

    chatSend.addEventListener('click', sendCurrent);
    chatInput.addEventListener('keydown', function(e){ 
        if (e.key === 'Enter') { 
            e.preventDefault(); 
            sendCurrent(); 
        } 
    });

    // 可选：显示欢迎语
    appendMessage('你好，我是智能助手。你可以咨询服务、报价或流程相关问题。', 'ai');
})();