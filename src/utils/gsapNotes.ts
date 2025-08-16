import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ScrambleTextPlugin } from "gsap/ScrambleTextPlugin";

gsap.registerPlugin(ScrollTrigger, ScrambleTextPlugin);

export function initNotesAnimations(notes: Record<string, string>) {
    const notesPanel = document.getElementById("notes-panel");
    if (!notesPanel) return;

    let currentNoteKey: string | null = null;

    Object.entries(notes).forEach(([rawKey, html]) => {
        const sectionId = rawKey.replace(/_/g, "-");
        const sectionEl = document.getElementById(sectionId);
        if (!sectionEl) return;

        ScrollTrigger.create({
            trigger: sectionEl,
            start: "top 25%",
            end: "bottom 0%",
            onEnter: () => showNoteIfNeeded(rawKey, html),
            onEnterBack: () => showNoteIfNeeded(rawKey, html),
            onLeave: () => hideNoteIfNeeded(rawKey),
            onLeaveBack: () => hideNoteIfNeeded(rawKey),
        });
    });

    function showNoteIfNeeded(key: string, html: string) {
        if (currentNoteKey === key) return;
        currentNoteKey = key;
        animateNoteHTML(html);
    }

    function hideNoteIfNeeded(key: string) {
        if (currentNoteKey !== key) return;
        currentNoteKey = null;
        gsap.to(notesPanel, { autoAlpha: 0, duration: 0.3 });
    }

    function animateNoteHTML(html: string) {
        // Clear and insert new content
        const temp = document.createElement("div");
        temp.innerHTML = html;
        notesPanel!.innerHTML = "";

        temp.childNodes.forEach((node) => {
            notesPanel!.appendChild(node.cloneNode(true));
        });

        // Animate text
        scrambleTextRecursively(notesPanel!);

        // Fade in
        gsap.to(notesPanel, { autoAlpha: 1, duration: 0.2 });
    }

    function scrambleTextRecursively(el: HTMLElement | ChildNode) {
        const textNodes: Text[] = [];

        const collectTextNodes = (node: HTMLElement | ChildNode) => {
            node.childNodes.forEach((child) => {
                if (child.nodeType === Node.TEXT_NODE && child.textContent?.trim()) {
                    textNodes.push(child as Text);
                } else if (child.nodeType === Node.ELEMENT_NODE) {
                    collectTextNodes(child);
                }
            });
        };

        collectTextNodes(el);

        textNodes.forEach((node, i) => {
            const parent = node.parentElement;
            const text = node.textContent?.trim();
            if (!parent || !text) return;

            node.textContent = "";

            gsap.to(node, {
                duration: 1.5,
                scrambleText: {
                    text,
                    chars: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?-",
                    revealDelay: 0.5,
                    speed: 0.2,
                },
                delay: i * 0.3,
            });
        });
    }
}
