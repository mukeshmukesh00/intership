// ... existing code ...

// Skill selection page functionality
function setupSkillSelection() {
    const container = $('#skills-container');
    if (!container.length) return;
    
    // Initialize tag functionality
    $('.skill-tag').click(function() {
        $(this).toggleClass('bg-primary bg-secondary');
        const skill = $(this).data('skill');
        const checkbox = $(`#skill-${skill}`);
        checkbox.prop('checked', !checkbox.prop('checked'));
        updateSelectedSkills();
    });
    
    // Update selected skills display
    function updateSelectedSkills() {
        const selected = [];
        $('input[name="skills"]:checked').each(function() {
            selected.push($(this).val());
        });
        
        const additional = $('#additional_skills').val().split(',')
            .map(skill => skill.trim())
            .filter(skill => skill !== '');
        
        const allSkills = [...selected, ...additional];
        $('#selected-skills-preview').html(
            allSkills.map(skill => `<span class="badge bg-primary me-1">${skill}</span>`).join('')
        );
    }
    
    // Set up event listeners
    $('input[name="skills"]').change(updateSelectedSkills);
    $('#additional_skills').on('input', updateSelectedSkills);
    
    // Initialize
    updateSelectedSkills();
}

$(document).ready(function() {
    // ... existing code ...
    
    // Setup skill selection page
    setupSkillSelection();
});