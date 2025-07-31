import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { initGsapAnimations } from "./gsapAnimations";

export function initializeGsap() {
  gsap.registerPlugin(ScrollTrigger);

  const recentPosts = document.querySelectorAll("#recent-posts li");
  const archives = document.querySelectorAll("#archives ul > *");

  if (recentPosts.length > 0) {
    initGsapAnimations(recentPosts);
  }
  if (archives.length > 0) {
    initGsapAnimations(archives);
  }
}
