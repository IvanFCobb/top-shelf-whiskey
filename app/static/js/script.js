// Nav Dropdown menu
document.addEventListener("DOMContentLoaded", function () {
  var toggleButton = document.getElementById("toggleButton");
  var navbarMenu = document.getElementById("navbarMenu");

  toggleButton.addEventListener("click", function () {
    navbarMenu.classList.toggle("hidden");
  });

  document.addEventListener("click", function (event) {
    if (
      !toggleButton.contains(event.target) &&
      !navbarMenu.contains(event.target)
    ) {
      navbarMenu.classList.add("hidden");
    }
  });
});

// Comment Dropdown menu

document.addEventListener("DOMContentLoaded", function () {
  const dropdownToggles = document.querySelectorAll("[data-dropdown-toggle]");

  dropdownToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const target = document.getElementById(this.dataset.dropdownToggle);
      if (target) {
        closeAllDropdownsExcept(target);
        target.classList.toggle("hidden");
      }
    });
  });

  window.addEventListener("click", function (event) {
    if (!event.target.matches("[data-dropdown-toggle]")) {
      closeAllDropdowns();
    }
  });
});

function closeAllDropdowns() {
  const dropdowns = document.getElementsByClassName("dropdown-content");
  for (let i = 0; i < dropdowns.length; i++) {
    const openDropdown = dropdowns[i];
    if (!openDropdown.classList.contains("hidden")) {
      openDropdown.classList.add("hidden");
    }
  }
}

function closeAllDropdownsExcept(exceptDropdown) {
  const dropdowns = document.getElementsByClassName("dropdown-content");
  for (let i = 0; i < dropdowns.length; i++) {
    const openDropdown = dropdowns[i];
    if (
      openDropdown !== exceptDropdown &&
      !openDropdown.classList.contains("hidden")
    ) {
      openDropdown.classList.add("hidden");
    }
  }
}

// reply to comment
document.addEventListener("DOMContentLoaded", function () {
  const replyButtons = document.querySelectorAll(".replyButton");

  replyButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      const formID = this.dataset.formId;
      const targetForm = document.getElementById(formID);

      if (targetForm) {
        closeAllReplyFormsExcept(targetForm);
        targetForm.classList.toggle("hidden");
      }
    });
  });
});

function closeAllReplyForms() {
  const replyForms = document.querySelectorAll(".replyForm");
  replyForms.forEach((form) => {
    if (!form.classList.contains("hidden")) {
      form.classList.add("hidden");
    }
  });
}

function closeAllReplyFormsExcept(exceptForm) {
  const replyForms = document.querySelectorAll(".replyForm");
  replyForms.forEach((form) => {
    if (form !== exceptForm && !form.classList.contains("hidden")) {
      form.classList.add("hidden");
    }
  });
}

// delete whiskey confirmation
function openModal(id, action) {
  console.log(`modal-${id}-${action}`);
  const modal = document.getElementById(`modal-${id}-${action}`);
  modal.style.display = "block";
}

function closeModal(id, action) {
  const modal = document.getElementById(`modal-${id}-${action}`);
  modal.style.display = "none";
}
