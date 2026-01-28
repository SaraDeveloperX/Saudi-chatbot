<template>
  <AppShell>
    <!-- Header with Back Button -->
    <template #header-content>
      <div class="h-full flex items-center px-4 md:px-6 relative justify-center">
         <!-- Back Button -->
         <button 
           @click="emit('close')"
           class="absolute right-4 md:right-6 p-2 text-white/90 hover:text-white bg-white/10 hover:bg-white/20 rounded-full transition-colors"
           aria-label="Back"
         >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 12H5"/>
              <path d="M12 19l-7-7 7-7"/>
            </svg>
         </button>
         
         <h1 class="text-xl font-semibold text-white">عن المشروع</h1>
      </div>
    </template>

    <div class="flex-1 overflow-y-auto px-4 py-8 pb-20 no-scrollbar" dir="rtl">
       <div class="max-w-2xl mx-auto space-y-10">
          
          <!-- SECTION 1 — عن المشروع -->
          <section>
             <h2 class="text-[#6CAD85] font-semibold text-lg mb-4">
                عن المشروع
             </h2>
             <p class="text-lg leading-relaxed text-gray-800 font-normal">
               يقدّم المشروع مساعدًا ذكيًا للإجابة عن الأسئلة المتعلقة بالمملكة العربية السعودية، وذلك بالاعتماد على قاعدة معرفية عربية منظّمة.
             </p>
          </section>

          <!-- SECTION 2 — نطاق الاستخدام -->
          <section>
             <h2 class="text-[#6CAD85] font-semibold text-lg mb-4">
                نطاق الاستخدام
             </h2>
             <p class="text-lg leading-relaxed text-gray-800 font-normal">
                يركّز المساعد على الموضوعات المرتبطة بالمملكة العربية السعودية فقط، ولا يقدّم معلومات خارج هذا النطاق.
             </p>
          </section>

          <!-- SECTION 3 — مصدر البيانات -->
          <section>
             <h2 class="text-[#6CAD85] font-semibold text-lg mb-4">
                مصدر البيانات
             </h2>
             <p class="text-gray-700 mb-4 leading-relaxed">
                يعتمد المشروع على قاعدة بيانات معرفية عربية مستخرجة من محتوى سعوديبيديا، والمتاحة عبر منصة Kaggle.
             </p>
             
             <a href="https://www.kaggle.com/datasets/ahmadhakami/saudipedia-arabic-q-and-a-knowledge-base" target="_blank" rel="noopener noreferrer" 
                class="inline-flex items-center gap-2 px-4 py-2 border border-[#6CAD85] text-[#6CAD85] rounded-lg hover:bg-[#6CAD85] hover:text-white transition-colors text-sm font-medium">
                <span>الاطلاع على مصدر البيانات</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
             </a>
          </section>

          <!-- SECTION 4 — ملاحظات -->
          <section class="border-t border-gray-100 pt-6 mt-8">
             <p class="text-sm text-gray-500 text-center leading-relaxed">
             تعتمد دقة الإجابات على المعلومات المتوفرة ضمن قاعدة المعرفة
             </p>
          </section>

       </div>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
import AppShell from '@/components/AppShell.vue'

const emit = defineEmits<{
  (e: 'close'): void
}>()
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

