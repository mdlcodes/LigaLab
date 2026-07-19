function toggleSection(sectionId){
    const section = document.getElementById(sectionId);
    const header = section.previousElementSibling;

    section.classList.toggle('active');

    if (header && header.classList.contains('accordion-header')){
        header.classList.toggle('active');
    }
}

