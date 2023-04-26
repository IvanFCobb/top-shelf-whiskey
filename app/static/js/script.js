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

// Create a function to open the modal
function openModal(whiskeyId, action) {
  const confirmationForm = document.getElementById("confirmationForm");

  const modal = document.getElementById("confirmationModal");
  const actionBtn = document.getElementById("actionBtn");

  if (action === "edit") {
    confirmationForm.action = "/whiskey/edit/" + whiskeyId;
    actionBtn.innerText = "Edit";
    actionBtn.classList.add("bg-blue-500", "hover:bg-blue-700");
    actionBtn.classList.remove("bg-red-500", "hover:bg-red-700");
  } else {
    confirmationForm.action = `/whiskey/delete` + whiskeyId;
    actionBtn.innerText = "Delete";
    actionBtn.classList.add("bg-red-500", "hover:bg-red-700");
    actionBtn.classList.remove("bg-blue-500", "hover:bg-blue-700");
  }

  modal.classList.add("visible");
}

// Create a function to close the modal
function closeModal() {
  const modal = document.getElementById("confirmationModal");
  modal.classList.remove("visible");
}
