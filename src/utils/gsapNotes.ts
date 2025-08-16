import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export function initNotesAnimations(notes: Record<string, string>) {
    gsap.registerPlugin(ScrollTrigger);

    const notesPanel = document.getElementById("notes-panel");
    if (!notesPanel) return;

    Object.entries(notes).forEach(([rawKey, html]) => {
        const sectionId = rawKey.replace(/_/g, "-");
        const sectionEl = document.getElementById(sectionId);
        if (!sectionEl) return;

        ScrollTrigger.create({
            trigger: sectionEl,
            start: "top center",
            end: "bottom center",
            onEnter: () => {
                notesPanel.innerHTML = html;
                gsap.to(notesPanel, { autoAlpha: 1, duration: 0.4 });
            },
            onEnterBack: () => {
                notesPanel.innerHTML = html;
                gsap.to(notesPanel, { autoAlpha: 1, duration: 0.4 });
            },
            onLeave: () => gsap.to(notesPanel, { autoAlpha: 0, duration: 0.3 }),
            onLeaveBack: () => gsap.to(notesPanel, { autoAlpha: 0, duration: 0.3 }),
        });
    });
}
