document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const fileList = document.getElementById('file-list');
    const uploadBtn = document.getElementById('upload-btn');
    const queryInput = document.getElementById('query-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');
    const resetBtn = document.getElementById('reset-btn');
    const toastContainer = document.getElementById('toast-container');

    const contextWrapper = document.getElementById('context-select-wrapper');
    const contextTrigger = document.getElementById('context-trigger');
    const contextOptions = document.getElementById('context-options');
    const contextCurrentText = document.getElementById('context-current-text');

    let currentContextFile = "";
    let selectedFiles = [];

    // Load initial files
    loadContextFiles();

    // Toggle Dropdown
    contextTrigger.addEventListener('click', (e) => {
        contextWrapper.classList.toggle('open');
        e.stopPropagation();
    });

    // Close Dropdown on outside click
    document.addEventListener('click', (e) => {
        if (!contextWrapper.contains(e.target)) {
            contextWrapper.classList.remove('open');
        }
    });

    async function loadContextFiles() {
        try {
            const res = await fetch('/api/files');
            if (res.ok) {
                const files = await res.json();
                updateContextDropdown(files);
            }
        } catch (e) {
            console.error('Failed to load files:', e);
        }
    }

    function updateContextDropdown(files) {
        // Clear options
        contextOptions.innerHTML = '';

        // Add All Documents
        addOption("", "All Documents", "fa-layer-group");

        files.forEach(f => {
            addOption(f, f, "fa-file-alt");
        });

        // Re-validate selection
        if (currentContextFile && !files.includes(currentContextFile)) {
            selectOption("");
        } else {
            selectOption(currentContextFile);
        }
    }

    function addOption(value, text, iconClass) {
        const div = document.createElement('div');
        div.className = 'custom-option';
        if (value === currentContextFile) div.classList.add('selected');
        div.dataset.value = value;
        div.innerHTML = `<i class="fas ${iconClass}"></i> ${text}`;

        div.addEventListener('click', (e) => {
            e.stopPropagation();
            selectOption(value);
            contextWrapper.classList.remove('open');
        });

        contextOptions.appendChild(div);
    }

    function selectOption(value) {
        currentContextFile = value;
        const options = contextOptions.querySelectorAll('.custom-option');
        let displayHtml = "All Documents";

        options.forEach(opt => {
            if (opt.dataset.value === value) {
                opt.classList.add('selected');
                displayHtml = opt.innerHTML; // Grab icon + text
            } else {
                opt.classList.remove('selected');
            }
        });

        // Update trigger text (just text or html? let's stick to text to avoid nesting issues in existing span)
        // Actually, let's just update the text content of the span but keep it clean
        // The span id is contextCurrentText. The option has innerHTML with an icon. 
        // We only want the text in the span, or the whole thing? 
        // The trigger html is: <i class="fas fa-database"></i> <span ...>Text</span>
        // Let's just update text of the span.

        // Extract text from the option html roughly or just use known values
        let text = "All Documents";
        if (value) text = value;

        contextCurrentText.textContent = text;
    }

    // --- File Handling ---
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
        // Reset input so same file can be selected again if needed
        fileInput.value = '';
    });

    function handleFiles(files) {
        const newFiles = Array.from(files);
        const existingNames = new Set(selectedFiles.map(f => f.name));

        let addedCount = 0;
        newFiles.forEach(f => {
            if (!existingNames.has(f.name)) {
                selectedFiles.push(f);
                addedCount++;
            }
        });

        if (addedCount > 0) renderFileList();
    }

    function renderFileList() {
        fileList.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const div = document.createElement('div');
            div.className = 'file-item';
            div.innerHTML = `
                <div style="flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                    <i class="fas fa-file-alt" style="margin-right:0.5rem; color:var(--accent-color)"></i>
                    ${file.name}
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem">
                    <span style="font-size:0.7em; opacity:0.7">${(file.size / 1024).toFixed(1)} KB</span>
                    <i class="fas fa-times" style="cursor:pointer; color:var(--error-color)" data-index="${index}"></i>
                </div>
            `;
            // Add remove listener
            div.querySelector('.fa-times').addEventListener('click', (e) => {
                e.stopPropagation();
                removeFile(index);
            });
            fileList.appendChild(div);
        });

        if (selectedFiles.length > 0) {
            uploadBtn.removeAttribute('disabled');
        } else {
            uploadBtn.setAttribute('disabled', 'true');
        }
    }

    function removeFile(index) {
        selectedFiles.splice(index, 1);
        renderFileList();
    }

    uploadBtn.addEventListener('click', async () => {
        if (selectedFiles.length === 0) return;

        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) throw new Error(await res.text());

            const data = await res.json();
            showToast(data.message || 'Upload successful', 'success');
            selectedFiles = [];
            renderFileList();
            // Refresh dropdown
            loadContextFiles();

            // Auto hide sidebar on successful upload for better experience
            if (window.innerWidth < 1024 || true) {
                setSidebarState(true);
            }
        } catch (err) {
            showToast(err.message || 'Upload failed', 'error');
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Process Documents';
        }
    });

    // Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const toggleIcon = sidebarToggle ? sidebarToggle.querySelector('i') : null;

    function setSidebarState(isClosed) {
        if (isClosed) {
            document.body.classList.add('sidebar-closed');
            if (toggleIcon) toggleIcon.className = 'fas fa-chevron-right';
        } else {
            document.body.classList.remove('sidebar-closed');
            if (toggleIcon) toggleIcon.className = 'fas fa-chevron-left';
        }
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            const isClosed = !document.body.classList.contains('sidebar-closed');
            setSidebarState(isClosed);
        });
    }

    // Auto-hide on mobile initially
    if (window.innerWidth < 768) {
        setSidebarState(true);
    }

    // --- Chat Handling ---
    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const text = queryInput.value.trim();
        if (!text) return;

        // User Message
        appendMessage('user', text);
        queryInput.value = '';
        queryInput.disabled = true;
        sendBtn.disabled = true;

        // Loading Indicator
        const loadingId = appendLoading();
        let msgDiv = null;
        let contentDiv = null;

        try {
            const selectedFile = currentContextFile || null;

            const response = await fetch('/api/chat/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: text,
                    history: [],
                    selected_file: selectedFile
                })
            });

            if (!response.ok) {
                removeMessage(loadingId);
                throw new Error(await response.text());
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let accumulatedText = "";

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                // On first chunk, remove loading and create message bubble
                if (!msgDiv) {
                    removeMessage(loadingId);
                    msgDiv = appendMessage('ai', '');
                    contentDiv = msgDiv.querySelector('.message-content');
                }

                const chunk = decoder.decode(value, { stream: true });
                accumulatedText += chunk;
                if (contentDiv) {
                    // Check if user is near the bottom before update
                    const isAtBottom = chatHistory.scrollHeight - chatHistory.scrollTop <= chatHistory.clientHeight + 100;

                    contentDiv.innerHTML = formatText(accumulatedText);

                    // Only auto-scroll if user was already at the bottom
                    if (isAtBottom) {
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    }
                }
            }

            // If response was empty or very fast
            if (!msgDiv) {
                removeMessage(loadingId);
                appendMessage('ai', '(No response received)');
            }

        } catch (err) {
            removeMessage(loadingId); // Ensure loading is removed on error
            appendMessage('ai', `Error: ${err.message}`);
        } finally {
            removeMessage(loadingId); // Cleanup in case of empty stream or other exits
            queryInput.disabled = false;
            sendBtn.disabled = false;
            queryInput.focus();
        }
    }

    function appendMessage(role, text, sources = []) {
        const div = document.createElement('div');
        div.className = `message ${role}`;

        let contentHtml = `<div class="message-content">${formatText(text)}`;
        if (sources && sources.length > 0) {
            contentHtml += `<div class="sources">
                <div class="sources-title">Sources</div>
                ${sources.map(s => `<div class="source-item">${s.source}</div>`).join('')}
            </div>`;
        }
        contentHtml += `</div>`;
        div.innerHTML = contentHtml;

        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return div;
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'message ai';
        div.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>`;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function formatText(text) {
        // Simple formatter for newlines and basic markdown-like bold
        // Enhanced: Handle basic code blocks or bolding
        let formatted = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        return formatted
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    // --- System (Modal Logic) ---
    const modal = document.getElementById('confirmation-modal');
    const modalCancel = document.getElementById('modal-cancel');
    const modalConfirm = document.getElementById('modal-confirm');

    function toggleModal(show) {
        if (show) {
            modal.classList.add('active');
        } else {
            modal.classList.remove('active');
        }
    }

    resetBtn.addEventListener('click', () => {
        toggleModal(true);
    });

    modalCancel.addEventListener('click', () => {
        toggleModal(false);
    });

    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) toggleModal(false);
    });

    modalConfirm.addEventListener('click', async () => {
        toggleModal(false);
        try {
            const res = await fetch('/api/reset', { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to reset');
            showToast('Knowledge base reset successfully', 'success');
            // clear chat
            chatHistory.innerHTML = '';
            appendMessage('ai', 'Memory reset. I am ready for new documents.');
            loadContextFiles(); // refresh list
        } catch (err) {
            showToast('Reset failed', 'error');
        }
    });

    function showToast(msg, type = 'success') {
        const div = document.createElement('div');
        div.className = `toast ${type}`;
        div.innerHTML = type === 'success' ? `<i class="fas fa-check-circle"></i> ${msg}` : `<i class="fas fa-exclamation-circle"></i> ${msg}`;
        toastContainer.appendChild(div);
        setTimeout(() => div.remove(), 3000);
    }

    // Initial Greeting
    appendMessage('ai', 'Hello! I am your Enterprise Knowledge Assistant. Upload documents or select a context to start.');
});
