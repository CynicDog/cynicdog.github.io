import { gsap } from "gsap";

export function initGsapAnimations(elements: NodeListOf<Element>) {

    gsap.from(elements, {
    scrollTrigger: {
      trigger: elements,
      start: "top 80%",
    },
    opacity: 0,
    y: 40,
    duration: 0.8,
    stagger: 0.3,
    ease: "power2.out",
  });
}
