$(document).ready(function () {
  const i18nData = {};

  const loadI18nData = async (lang) => {
    if (!i18nData[lang]) {
      try {
        const response = await fetch(`lang/${lang}.json`);
        if (!response.ok) {
          throw new Error(`Failed to load ${lang} language file`);
        }
        i18nData[lang] = await response.json();
        console.log(`Loaded ${lang} language file:`, i18nData[lang]);
      } catch (error) {
        console.error("Error loading translation:", error);
      }
    }
    return i18nData[lang];
  };

  const updateContent = (lang) => {
    loadI18nData(lang).then((data) => {
      $("[data-i18n]").each(function () {
        const key = $(this).data("i18n");
        const keys = key.split(".");
        let value = data;
        keys.forEach((k) => {
          value = value ? value[k] : null;
        });
        if (value) {
          $(this).text(value);
        } else {
          console.warn(`No translation found for key: ${key}`);
        }
      });
    });
  };

  $("#languageSwitcher").on("change", function () {
    const selectedLang = $(this).val();
    updateContent(selectedLang);
  });

  // Initialize content with the default language (English)
  updateContent("en");
});
