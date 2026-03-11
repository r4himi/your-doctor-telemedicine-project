async function translatePage(targetLang) {
    const elements = document.querySelectorAll('[data-translate]');

    for (const el of elements) {
        if (!el.dataset.original) {
            el.dataset.original = el.textContent.trim();
        }

        const original = el.dataset.original;
        if (!original) continue;

        try {
            const res = await fetch("/translate-api/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: original, target: targetLang })
            });

            if (!res.ok) {
                console.error("API Error:", res.status, await res.text());
                continue;
            }

            const data = await res.json();
            const translated = data.translatedText || data.translation || "";

            if (translated) {
                el.textContent = translated; // only replace text
            }
        } catch (err) {
            console.error("Translation error:", err);
        }
    }
}