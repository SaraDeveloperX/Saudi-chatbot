<template>
  <div class="app-shell">
    <!-- Responsive Phone Container -->
    <div class="phone-container">
      
      <!-- Solid Header Block -->
      <div class="header-block">
        <slot name="header-content" />
      </div>

      <!-- Overlapping White Card -->
      <div class="content-card" dir="rtl">
        <div class="card-content-fade">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  min-height: 100dvh;
  background-color: #F4F6F8;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  font-family: 'Tajawal', sans-serif;
}

.phone-container {
  width: 100%;
  background-color: #F4F6F8;
  min-height: 100vh;
  min-height: 100dvh;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}


.header-block {
  height: 140px;
  width: 100%;
  background-color: #6CAD85;
  flex-shrink: 0;
  position: relative;
  
  /* Force Static */
  animation: none !important;
  transition: none !important;
  transform: none !important;
  opacity: 1 !important;
}

.content-card {
  flex: 1;
  width: 100%;
  background-color: white;
  position: relative;
  display: flex;
  flex-direction: column;
  margin-top: -30px;
  border-top-left-radius: 40px;
  border-top-right-radius: 40px;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
  padding: 24px 16px;
  
  /* Ensure container is solid and static */
  opacity: 1 !important;
  background-color: white !important;
  animation: none !important;
}

.card-content-fade {
  /* Animate ONLY the content, not the container background */
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  flex: 1;
  animation: contentFadeIn 0.35s ease-out both;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .card-content-fade {
    animation: none;
  }
}

/* Mobile defaults (Base styles) */
.phone-container {
  width: 100%;
  background-color: transparent;
  min-height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: visible;
  max-width: none;
  border-radius: 0;
  margin: 0;
  box-shadow: none;
  padding-bottom: env(safe-area-inset-bottom);
}

.header-block {
  height: 140px; /* Fixed height */
  width: 100%;
  background-color: #6CAD85;
  flex-shrink: 0;
  position: relative;
  border-radius: 0 !important;
}

.content-card {
  flex: 1;
  width: 100%;
  background-color: white;
  position: relative;
  display: flex;
  flex-direction: column;
  margin-top: -36px; /* -36px overlap */
  
  /* Mobile: Top rounded only */
  border-top-left-radius: 40px;
  border-top-right-radius: 40px;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  
  box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
  padding: 24px 20px; /* Mobile padding 20-24px */
}

/* Tablet & Desktop (Combined Override to ensure full width) */
@media (min-width: 431px) {
  .phone-container {
    max-width: none; /* Full width */
    min-height: 100vh;
    margin: 0;
    border-radius: 0;
    box-shadow: none;
    overflow: visible;
  }
  
  .content-card {
    /* Maintain top overlap and rounding */
    border-top-left-radius: 40px;
    border-top-right-radius: 40px;
    /* Reset bottom rounding to 0 for full-screen feel, or keep it? 
       User said: "Keep rounded corners ONLY on the white card top corners"
       So bottom should be square if it goes to bottom of screen. */
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    
    /* Adjust shadow/padding if needed, but keep full width */
    box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    
    /* Keep the larger padding for tablet/desktop */
    padding: 32px 28px;
    
    /* Subtle hover effect on desktop */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .content-card:hover {
     transform: translateY(-2px);
     box-shadow: 0 -6px 25px rgba(0,0,0,0.08); /* Slightly increased shadow */
  }
}
</style>
