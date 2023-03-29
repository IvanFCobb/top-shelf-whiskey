$(function () {
  $(".toggle-menu").click(function () {
    $(".navbar-menu").toggleClass("hidden");
  });
});

// script for animating the cards on load

function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();

  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

function animateCards() {
  const cards = document.querySelectorAll(".card");

  cards.forEach((card) => {
    if (isElementInViewport(card)) {
      card.style.opacity = "1";

      card.style.transform = "translateX(0)";
    }
  });
}

window.addEventListener("scroll", animateCards);
window.addEventListener("load", animateCards);
