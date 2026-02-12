import { useState, useEffect } from "react";
import "@/App.css";
import { motion, AnimatePresence } from "framer-motion";
import { Check, ChevronRight, LogOut, Copy, ArrowLeft, ArrowRight, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Toaster, toast } from "sonner";
import contentData from "@/data/contentData.json";

// Image Lightbox Component
const ImageLightbox = ({ images, onClose }) => {
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose();
    };
    // Prevent body scroll when lightbox is open
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', handleEsc);
    return () => {
      document.body.style.overflow = 'auto';
      window.removeEventListener('keydown', handleEsc);
    };
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-[9999] bg-black/80 flex items-center justify-center"
      style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0 }}
      onClick={onClose}
      data-testid="image-lightbox"
    >
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-2 bg-white/10 hover:bg-white/20 rounded-full transition-colors z-[10000]"
        data-testid="lightbox-close"
      >
        <X className="w-6 h-6 text-white" />
      </button>
      <div className="flex gap-4 items-center justify-center" onClick={(e) => e.stopPropagation()}>
        {images.map((img, idx) => (
          <img
            key={idx}
            src={img.src}
            alt={img.alt}
            className="max-h-[85vh] object-contain rounded-lg shadow-2xl"
            style={{ maxWidth: images.length > 1 ? '45vw' : '90vw' }}
          />
        ))}
      </div>
    </div>
  );
};

// Stepper Component
const Stepper = ({ currentStep, steps }) => {
  return (
    <div className="flex items-center justify-center gap-1 md:gap-2 mb-6 md:mb-8 px-1 md:px-2" data-testid="stepper">
      {steps.map((step, index) => {
        const isCompleted = index < currentStep;
        const isActive = index === currentStep;
        const stepNumber = index + 1;

        return (
          <div key={step.id} className="flex items-center flex-shrink-0">
            <div className="flex flex-col items-center min-w-[60px] md:min-w-[80px]">
              <motion.div
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className={`
                  w-7 h-7 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-full flex items-center justify-center text-[10px] sm:text-xs md:text-sm font-semibold
                  transition-all duration-300 shadow-sm
                  ${isCompleted ? 'bg-[#0F172A] text-white' : ''}
                  ${isActive ? 'bg-[#FF7870] text-white ring-2 md:ring-4 ring-pink-100' : ''}
                  ${!isCompleted && !isActive ? 'bg-white border-2 border-slate-200 text-slate-400' : ''}
                `}
                data-testid={`stepper-step-${stepNumber}`}
              >
                {isCompleted ? <Check className="w-3 h-3 sm:w-4 sm:h-4 md:w-5 md:h-5" /> : stepNumber}
              </motion.div>
              <span className={`text-[9px] sm:text-[10px] md:text-xs mt-1 md:mt-2 font-medium text-center leading-tight ${isActive ? 'text-[#0F172A]' : 'text-slate-400'}`}>
                {step.label}
              </span>
              <span className="text-[7px] md:text-[10px] text-slate-400 hidden sm:block">{step.sublabel}</span>
            </div>
            {index < steps.length - 1 && (
              <ChevronRight className="w-2 h-2 sm:w-3 sm:h-3 md:w-4 md:h-4 mx-0.5 sm:mx-1 md:mx-2 text-slate-300 mt-[-16px] sm:mt-[-18px] md:mt-[-20px]" />
            )}
          </div>
        );
      })}
    </div>
  );
};

// Tab Component
const TabButton = ({ active, children, onClick, testId }) => (
  <button
    onClick={onClick}
    data-testid={testId}
    className={`
      px-2.5 py-1.5 sm:px-4 sm:py-2 md:px-6 md:py-2.5 rounded-full text-[11px] sm:text-xs md:text-sm font-medium transition-all duration-200
      whitespace-nowrap flex-shrink-0
      ${active 
        ? 'bg-[#0F172A] text-white shadow-md' 
        : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'
      }
    `}
  >
    {children}
  </button>
);

// Copy Button Component
const CopyButton = ({ text, label }) => {
  const handleCopy = async (e) => {
    e.stopPropagation();
    try {
      await navigator.clipboard.writeText(text);
      toast.success(`${label || 'Text'} copied!`);
    } catch (err) {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand("copy");
        toast.success(`${label || 'Text'} copied!`);
      } catch (e) {
        toast.error("Could not copy");
      }
      document.body.removeChild(textArea);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="p-1.5 hover:bg-slate-100 rounded-md transition-colors"
      data-testid={`copy-${label?.toLowerCase().replace(/\s+/g, '-') || 'text'}`}
    >
      <Copy className="w-4 h-4 text-slate-400 hover:text-slate-600" />
    </button>
  );
};

// Visual Style Step
const VisualStyleStep = ({ visualStyles, selectedStyle, onSelect, onImageClick }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="animate-fadeIn"
    >
      <h2 className="text-lg md:text-2xl font-bold text-center mb-2 text-[#0F172A] px-2">Choose Your Visual Style</h2>
      <p className="text-slate-500 text-center mb-4 md:mb-8 text-sm md:text-base px-4">Select a visual style that matches your content theme</p>
      
      {/* Mobile: Card Layout */}
      <div className="md:hidden space-y-3">
        {visualStyles.map((style) => (
          <motion.div
            key={style.id}
            whileTap={{ scale: 0.98 }}
            whileHover={{ backgroundColor: 'rgba(255, 120, 112, 0.05)' }}
            className={`bg-white rounded-xl border border-slate-100 shadow-sm p-3 sm:p-4 cursor-pointer transition-colors active:scale-[0.98] ${
              selectedStyle?.id === style.id ? 'bg-pink-50/50 border-pink-200 ring-2 ring-pink-100' : ''
            }`}
            onClick={() => onSelect(style)}
            data-testid={`visual-style-${style.id}`}
          >
            <div className="flex items-start gap-2 sm:gap-3">
              <Checkbox 
                checked={selectedStyle?.id === style.id}
                onCheckedChange={() => onSelect(style)}
                data-testid={`visual-style-checkbox-${style.id}`}
                className="mt-0.5 sm:mt-1"
              />
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm text-[#0F172A] mb-2 leading-tight">{style.title}</p>
                <div className="flex gap-2 overflow-x-auto pb-2 -mx-1 px-1">
                  {style.images.map((img, idx) => (
                    <img
                      key={idx}
                      src={img}
                      alt={`${style.title} preview ${idx + 1}`}
                      className="w-20 h-28 sm:w-24 sm:h-32 flex-shrink-0 object-cover rounded-lg border border-slate-200 cursor-zoom-in hover:border-[#FF7870] transition-all"
                      onClick={(e) => {
                        e.stopPropagation();
                        onImageClick(style.images.map((imgUrl, i) => ({ 
                          src: imgUrl, 
                          alt: `${style.title} preview ${i + 1}` 
                        })));
                      }}
                      data-testid={`image-${style.id}-${idx}`}
                    />
                  ))}
                </div>
                {style.info && (
                  <p className="text-xs text-slate-500 italic mt-2">{style.info}</p>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Desktop: Table Layout */}
      <div className="hidden md:block bg-white rounded-2xl border border-slate-100 shadow-xl shadow-slate-200/50 overflow-hidden">
        <div className="grid grid-cols-[60px_1fr_2fr] bg-[#0F172A] text-white text-xs font-bold uppercase tracking-wider">
          <div className="px-4 py-3">Select</div>
          <div className="px-4 py-3">Images</div>
          <div className="px-4 py-3">Info</div>
        </div>
        
        <div className="divide-y divide-slate-50">
          {visualStyles.map((style) => (
            <motion.div
              key={style.id}
              whileHover={{ backgroundColor: 'rgba(255, 120, 112, 0.05)' }}
              className={`grid grid-cols-[60px_1fr_2fr] items-center cursor-pointer transition-colors ${
                selectedStyle?.id === style.id ? 'bg-pink-50/50' : ''
              }`}
              onClick={() => onSelect(style)}
              data-testid={`visual-style-${style.id}`}
            >
              <div className="px-4 py-4 flex justify-center">
                <Checkbox 
                  checked={selectedStyle?.id === style.id}
                  onCheckedChange={() => onSelect(style)}
                  data-testid={`visual-style-checkbox-${style.id}`}
                />
              </div>
              <div className="px-4 py-4">
                <p className="font-semibold text-sm text-[#0F172A] mb-2">{style.title}</p>
                <div className="flex gap-3">
                  {style.images.map((img, idx) => (
                    <img
                      key={idx}
                      src={img}
                      alt={`${style.title} preview ${idx + 1}`}
                      className="w-44 h-56 object-cover rounded-lg border border-slate-200 cursor-zoom-in hover:border-[#FF7870] hover:shadow-md transition-all"
                      onClick={(e) => {
                        e.stopPropagation();
                        onImageClick(style.images.map((imgUrl, i) => ({ 
                          src: imgUrl, 
                          alt: `${style.title} preview ${i + 1}` 
                        })));
                      }}
                      data-testid={`image-${style.id}-${idx}`}
                    />
                  ))}
                </div>
              </div>
              <div className="px-4 py-4">
                {style.info && (
                  <p className="text-sm text-slate-500 italic">{style.info}</p>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};

// Hook Step
const HookStep = ({ hooks, selectedHook, onSelect, selectedStyle }) => {
  // Check if selected style is a "Mistakes" style
  const isMistakeStyle = selectedStyle?.title?.toLowerCase().includes('mistake');
  
  // Different categories based on style type
  const regularCategories = ["Ex TikTok", "Professor", "Official TikTok", "Experienced", "Journalist", "New TikTok Algorithm", "Learnings", "AI Tips"];
  const mistakeCategories = ["Ex TikTok - Mistakes", "Professor - Mistakes", "Official TikTok - Mistakes", "Experienced - Mistakes", "Learnings - Mistakes"];
  
  const categories = isMistakeStyle ? mistakeCategories : regularCategories;
  const displayCategories = isMistakeStyle 
    ? ["Ex TikTok", "Professor", "Official TikTok", "Experienced", "Learnings"]
    : regularCategories;
  
  const [activeCategory, setActiveCategory] = useState(categories[0]);
  
  // Update active category when style changes
  useEffect(() => {
    const newCategories = isMistakeStyle 
      ? ["Ex TikTok - Mistakes", "Professor - Mistakes", "Official TikTok - Mistakes", "Experienced - Mistakes", "Learnings - Mistakes"]
      : ["Ex TikTok", "Professor", "Official TikTok", "Experienced", "Journalist", "New TikTok Algorithm", "Learnings", "AI Tips"];
    setActiveCategory(newCategories[0]);
  }, [isMistakeStyle]);
  
  const filteredHooks = hooks.filter(h => h.category === activeCategory);

  const handleCategoryClick = (displayCat, idx) => {
    if (isMistakeStyle) {
      setActiveCategory(mistakeCategories[idx]);
    } else {
      setActiveCategory(displayCat);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <h2 className="text-lg md:text-2xl font-bold text-center mb-2 text-[#0F172A] px-2">Choose Your Hook</h2>
      <p className="text-slate-500 text-center mb-2 text-sm md:text-base px-4">Select a hook that will grab your audience's attention</p>
      {selectedStyle && (
        <p className="text-[#FF7870] text-center text-xs md:text-sm mb-4 md:mb-6 px-4">
          Showing only {isMistakeStyle ? 'Mistake' : selectedStyle.title.replace(':', '')} hooks based on your visual style selection
        </p>
      )}
      
      <div className="flex flex-wrap gap-1.5 sm:gap-2 justify-center mb-4 md:mb-6 px-2">
        {displayCategories.map((cat, idx) => (
          <TabButton
            key={cat}
            active={isMistakeStyle ? activeCategory === mistakeCategories[idx] : activeCategory === cat}
            onClick={() => handleCategoryClick(cat, idx)}
            testId={`hook-tab-${cat.toLowerCase().replace(/\s+/g, '-')}`}
          >
            {cat}
          </TabButton>
        ))}
      </div>

      {/* Mobile: Card Layout */}
      <div className="md:hidden space-y-2">
        {filteredHooks.map((hook) => (
          <motion.div
            key={hook.id}
            whileTap={{ scale: 0.98 }}
            whileHover={{ backgroundColor: 'rgba(255, 120, 112, 0.05)' }}
            className={`bg-white rounded-xl border border-slate-100 shadow-sm p-3 sm:p-4 cursor-pointer transition-colors active:scale-[0.98] ${
              selectedHook?.id === hook.id ? 'bg-pink-50/50 border-pink-200 ring-2 ring-pink-100' : ''
            }`}
            onClick={() => onSelect(hook)}
            data-testid={`hook-${hook.id}`}
          >
            <div className="flex items-start gap-2 sm:gap-3">
              <Checkbox 
                checked={selectedHook?.id === hook.id}
                onCheckedChange={() => onSelect(hook)}
                data-testid={`hook-checkbox-${hook.id}`}
                className="mt-0.5"
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-[#0F172A] mb-2 leading-relaxed">{hook.idea}</p>
                <div className="flex flex-wrap gap-2 text-xs">
                  {hook.reference_links && hook.reference_links !== '-' && (
                    <a href={hook.reference_links} target="_blank" rel="noopener noreferrer" className="text-[#FF7870] hover:underline">
                      View Reference →
                    </a>
                  )}
                  {hook.notes && (
                    <span className="text-slate-500">{hook.notes}</span>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Desktop: Table Layout */}
      <div className="hidden md:block bg-white rounded-2xl border border-slate-100 shadow-xl shadow-slate-200/50 overflow-hidden">
        <div className="grid grid-cols-[60px_80px_1fr_150px_100px] bg-[#0F172A] text-white text-xs font-bold uppercase tracking-wider">
          <div className="px-4 py-3">Select</div>
          <div className="px-4 py-3">Rank</div>
          <div className="px-4 py-3">Idea</div>
          <div className="px-4 py-3">Reference Links</div>
          <div className="px-4 py-3">Notes</div>
        </div>
        
        <div className="divide-y divide-slate-50">
          {filteredHooks.map((hook) => (
            <motion.div
              key={hook.id}
              whileHover={{ backgroundColor: 'rgba(255, 120, 112, 0.05)' }}
              className={`grid grid-cols-[60px_80px_1fr_150px_100px] items-center cursor-pointer transition-colors ${
                selectedHook?.id === hook.id ? 'bg-pink-50/50' : ''
              }`}
              onClick={() => onSelect(hook)}
              data-testid={`hook-${hook.id}`}
            >
              <div className="px-4 py-4 flex justify-center">
                <Checkbox 
                  checked={selectedHook?.id === hook.id}
                  onCheckedChange={() => onSelect(hook)}
                  data-testid={`hook-checkbox-${hook.id}`}
                />
              </div>
              <div className="px-4 py-4 text-sm text-slate-500">
                {hook.rank || '-'}
              </div>
              <div className="px-4 py-4 text-sm text-[#0F172A]">
                {hook.idea}
              </div>
              <div className="px-4 py-4 text-sm text-slate-500">
                {hook.reference_links && hook.reference_links !== '-' ? (
                  <a href={hook.reference_links} target="_blank" rel="noopener noreferrer" className="text-[#FF7870] hover:underline truncate block max-w-[130px]">
                    View
                  </a>
                ) : '-'}
              </div>
              <div className="px-4 py-4 text-sm text-slate-500">
                {hook.notes || '-'}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};

// Script Step
const ScriptStep = ({ scripts, selectedScripts, onSelect, currentScriptIndex, setCurrentScriptIndex, selectedStyle }) => {
  // Check if selected style is a "Mistakes" style
  const isMistakeStyle = selectedStyle?.title?.toLowerCase().includes('mistake');
  
  // Determine which tab should be active based on current script index and previous selections
  const getDefaultTab = (index) => {
    if (index === 3) return "viral_plug"; // Script 4 must be Viral Plug
    if (index === 0) return "choice"; // Script 1: user chooses between other and engagement
    if (index === 1) {
      // Script 2: show the opposite of what was chosen in Script 1
      const script1Type = selectedScripts[0]?.type;
      return script1Type === "engagement" ? "other" : "engagement";
    }
    if (index === 2) return "other"; // Script 3: other scripts
    if (index === 4) return "other"; // Script 5: other scripts
    return "other";
  };
  
  const [activeTab, setActiveTab] = useState("other");
  
  // Update tab when currentScriptIndex changes
  useEffect(() => {
    // Determine which tab should be active based on current script index
    if (currentScriptIndex === 3) {
      setActiveTab(isMistakeStyle ? "mistake_viral" : "viral_plug");
    } else if (currentScriptIndex === 0) {
      // Default for script 1: "other" for normal, "mistake" for mistake styles
      setActiveTab(isMistakeStyle ? "mistake" : "other");
    } else if (currentScriptIndex === 1) {
      // Script 2: show the opposite of what was chosen in Script 1
      if (isMistakeStyle) {
        const script1Type = selectedScripts[0]?.type;
        setActiveTab(script1Type === "mistake_engagement" ? "mistake" : "mistake_engagement");
      } else {
        const script1Type = selectedScripts[0]?.type;
        setActiveTab(script1Type === "engagement" ? "other" : "engagement");
      }
    } else if (currentScriptIndex === 2 || currentScriptIndex === 4) {
      setActiveTab(isMistakeStyle ? "mistake" : "other");
    }
  }, [currentScriptIndex, selectedScripts, isMistakeStyle]);
  
  // Get filtered scripts based on active tab and style type
  const getFilteredScripts = () => {
    // For Mistake styles, Script 1 uses activeTab (mistake or mistake_engagement)
    if (isMistakeStyle && currentScriptIndex === 0) {
      return scripts.filter(s => s.type === activeTab);
    }
    // For Mistake styles, Script 2 shows the opposite of Script 1
    if (isMistakeStyle && currentScriptIndex === 1) {
      const script1Type = selectedScripts[0]?.type;
      const targetType = script1Type === "mistake_engagement" ? "mistake" : "mistake_engagement";
      return scripts.filter(s => s.type === targetType);
    }
    // For Mistake styles, Scripts 3, 5 show mistake scripts
    if (isMistakeStyle && (currentScriptIndex === 2 || currentScriptIndex === 4)) {
      return scripts.filter(s => s.type === "mistake");
    }
    // For Mistake styles, Script 4 shows mistake_viral
    if (isMistakeStyle && currentScriptIndex === 3) {
      return scripts.filter(s => s.type === "mistake_viral");
    }
    return scripts.filter(s => s.type === activeTab);
  };
  
  const filteredScripts = getFilteredScripts();
  
  // Get the type label for a script position
  const getScriptTypeLabel = (index, script) => {
    if (index === 3) {
      return script?.type === "mistake_viral" ? "Mistake Viral Plug" : "Viral Plug";
    }
    if (script?.type === "engagement") return "Engagement Trigger";
    if (script?.type === "mistake_engagement") return "Mistake Engagement";
    if (script?.type === "mistake") return "Mistake Script";
    if (script?.type === "mistake_viral") return "Mistake Viral Plug";
    return "Other Script";
  };

  // Get the subtitle for current script
  const getScriptSubtitle = () => {
    if (isMistakeStyle) {
      if (currentScriptIndex === 0) return "Choose: Mistake Scripts OR Mistake Engagement";
      if (currentScriptIndex === 1) {
        const script1Type = selectedScripts[0]?.type;
        return script1Type === "mistake_engagement" ? "Mistake Scripts (auto-selected)" : "Mistake Engagement (auto-selected)";
      }
      if (currentScriptIndex === 2) return "Mistake Scripts";
      if (currentScriptIndex === 3) return "Mistake Viral Plug (Mistake Style)";
      if (currentScriptIndex === 4) return "Mistake Scripts";
    }
    if (currentScriptIndex === 0) return "Choose: Other Scripts OR Engagement Triggers";
    if (currentScriptIndex === 1) {
      const script1Type = selectedScripts[0]?.type;
      return script1Type === "engagement" ? "Other Scripts (auto-selected)" : "Engagement Triggers (auto-selected)";
    }
    if (currentScriptIndex === 2) return "Other Scripts";
    if (currentScriptIndex === 3) return "Viral Plug Required";
    if (currentScriptIndex === 4) return "Other Scripts";
    return "";
  };

  // Check if a script can be selected for current position
  const canSelectScript = (script) => {
    // Check if already selected
    const isSelected = selectedScripts.some(s => s?.id === script.id);
    if (isSelected) return false;
    
    // Script 4: For Mistake styles use mistake_viral, otherwise viral_plug
    if (currentScriptIndex === 3) {
      return isMistakeStyle ? script.type === "mistake_viral" : script.type === "viral_plug";
    }
    // Mistake viral only for Script 4 in Mistake styles
    if (script.type === "mistake_viral") {
      return isMistakeStyle && currentScriptIndex === 3;
    }
    // Viral plug only for Script 4 in normal styles
    if (script.type === "viral_plug") {
      return !isMistakeStyle && currentScriptIndex === 3;
    }
    
    // For Mistake styles, Script 1 can choose mistake or mistake_engagement
    if (isMistakeStyle && currentScriptIndex === 0) {
      return script.type === "mistake" || script.type === "mistake_engagement";
    }
    // For Mistake styles, Script 2 must be opposite of Script 1
    if (isMistakeStyle && currentScriptIndex === 1) {
      const script1Type = selectedScripts[0]?.type;
      return script.type !== script1Type;
    }
    // For Mistake styles, Scripts 3, 5 show mistake scripts
    if (isMistakeStyle && (currentScriptIndex === 2 || currentScriptIndex === 4)) {
      return script.type === "mistake";
    }
    
    // Script 1: can choose either other or engagement
    if (currentScriptIndex === 0) {
      return script.type === "other" || script.type === "engagement";
    }
    
    // Script 2: must be opposite of script 1
    if (currentScriptIndex === 1) {
      const script1Type = selectedScripts[0]?.type;
      return script.type !== script1Type;
    }
    
    // Script 3 and 5: only other scripts (engagement already used in script 1 or 2)
    if (currentScriptIndex === 2 || currentScriptIndex === 4) {
      return script.type === "other";
    }
    
    return true;
  };

  // Get disabled reason for a script
  const getDisabledReason = (script) => {
    if (selectedScripts.some(s => s?.id === script.id)) {
      return "Already selected";
    }
    // For Mistake styles, Script 2 must be opposite of Script 1
    if (isMistakeStyle && currentScriptIndex === 1) {
      const script1Type = selectedScripts[0]?.type;
      if (script.type === script1Type) {
        return `Script 1 already selected ${script1Type === "mistake_engagement" ? "Mistake Engagement" : "Mistake Script"}`;
      }
    }
    // For Mistake styles, Scripts 3, 5 must be mistake
    if (isMistakeStyle && (currentScriptIndex === 2 || currentScriptIndex === 4) && script.type !== "mistake") {
      return "Mistake style requires Mistake Scripts";
    }
    if (currentScriptIndex === 1) {
      const script1Type = selectedScripts[0]?.type;
      if (script.type === script1Type) {
        return `Script 1 already selected ${script1Type === "engagement" ? "Engagement Trigger" : "Other Script"}`;
      }
    }
    if (currentScriptIndex === 2 || currentScriptIndex === 4) {
      if (script.type === "engagement") {
        return "Engagement Trigger already used";
      }
    }
    return "";
  };

  const handleRemoveScript = (index) => {
    onSelect(undefined, index, true);
    setCurrentScriptIndex(index);
  };

  // Get available types for Script 1 choice buttons
  const getAvailableTypesForScript1 = () => {
    return [
      { type: "other", label: "Other Scripts" },
      { type: "engagement", label: "Engagement Triggers" }
    ];
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <h2 className="text-lg md:text-2xl font-bold text-center mb-2 text-[#0F172A] px-2">Choose Your 5 Scripts</h2>
      <p className="text-slate-500 text-center mb-2 text-xs md:text-sm px-3">
        {isMistakeStyle 
          ? "Mistake Style: Script 1 = Mistake Engagement • Scripts 2,3,5 = Mistake Scripts • Script 4 = Mistake Viral Plug"
          : "Script 1: Choose type • Script 2: Auto-filled opposite • Script 4: Viral Plug • Scripts 3 & 5: Other Scripts"}
      </p>
      
      {/* Script Selection Progress */}
      <div className="bg-white rounded-xl md:rounded-2xl border border-slate-100 shadow-lg p-3 sm:p-4 md:p-6 mb-4 md:mb-8">
        <h3 className="text-xs sm:text-sm font-semibold text-center text-slate-600 mb-3 md:mb-4">Script Selection Progress</h3>
        <div className="flex items-center justify-center gap-1 sm:gap-2">
          {[0, 1, 2, 3, 4].map((idx) => {
            const script = selectedScripts[idx];
            const isActive = idx === currentScriptIndex;
            const isCompleted = script !== undefined;
            
            return (
              <div key={idx} className="flex items-center">
                <div className="flex flex-col items-center min-w-[48px] sm:min-w-[60px] md:min-w-[80px]">
                  <div
                    className={`
                      w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 rounded-full flex items-center justify-center text-[9px] sm:text-[10px] md:text-xs font-semibold cursor-pointer transition-all
                      ${isCompleted ? 'bg-[#0F172A] text-white' : ''}
                      ${isActive && !isCompleted ? 'bg-[#FF7870] text-white ring-2 ring-pink-200' : ''}
                      ${!isActive && !isCompleted ? 'bg-white border-2 border-slate-200 text-slate-400' : ''}
                    `}
                    onClick={() => !isCompleted && setCurrentScriptIndex(idx)}
                  >
                    {isCompleted ? <Check className="w-2.5 h-2.5 sm:w-3 sm:h-3 md:w-4 md:h-4" /> : idx + 1}
                  </div>
                  <span className="text-[7px] sm:text-[8px] md:text-[10px] mt-1 font-medium text-slate-700">Script {idx + 1}</span>
                  <span className="text-[6px] md:text-[9px] text-slate-400 text-center hidden sm:block truncate max-w-[70px]">
                    {getScriptTypeLabel(idx, script)}
                  </span>
                  {isCompleted && (
                    <button
                      onClick={() => handleRemoveScript(idx)}
                      className="text-[7px] sm:text-[8px] md:text-[10px] text-[#FF7870] hover:underline mt-0.5 font-medium"
                      data-testid={`remove-script-${idx}`}
                    >
                      Remove
                    </button>
                  )}
                </div>
                {idx < 4 && <ChevronRight className="w-1.5 h-1.5 sm:w-2 sm:h-2 md:w-3 md:h-3 mx-0 sm:mx-0.5 md:mx-1 text-slate-300" />}
              </div>
            );
          })}
        </div>
      </div>

      <h3 className="text-lg font-semibold mb-2 text-[#0F172A]">
        Select Script {currentScriptIndex + 1}
      </h3>
      <p className="text-sm text-slate-500 mb-4">{getScriptSubtitle()}</p>
      
      {/* Tab Buttons - Only show for Script 1 */}
      {currentScriptIndex === 0 && (
        <div className="flex gap-2 mb-4 md:mb-6 overflow-x-auto pb-2 -mx-1 px-1 scrollbar-hide">
          {isMistakeStyle ? (
            <>
              <TabButton
                active={activeTab === "mistake" || selectedScripts[0]?.type === "mistake"}
                onClick={() => setActiveTab("mistake")}
                testId="scripts-tab-mistake"
              >
                Mistake Scripts
              </TabButton>
              <TabButton
                active={activeTab === "mistake_engagement" || selectedScripts[0]?.type === "mistake_engagement"}
                onClick={() => setActiveTab("mistake_engagement")}
                testId="scripts-tab-mistake-engagement"
              >
                Mistake Engagement
              </TabButton>
            </>
          ) : (
            <>
              <TabButton
                active={activeTab === "other" || selectedScripts[0]?.type === "other"}
                onClick={() => setActiveTab("other")}
                testId="scripts-tab-other"
              >
                Other Scripts
              </TabButton>
              <TabButton
                active={activeTab === "engagement" || selectedScripts[0]?.type === "engagement"}
                onClick={() => setActiveTab("engagement")}
                testId="scripts-tab-engagement"
              >
                Engagement Triggers
              </TabButton>
            </>
          )}
        </div>
      )}

      {/* For Script 2, show what type is being auto-selected */}
      {currentScriptIndex === 1 && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
          {isMistakeStyle ? (
            <p className="text-sm text-blue-700">
              Script 1 selected: <span className="font-semibold">{selectedScripts[0]?.type === "mistake_engagement" ? "Mistake Engagement" : "Mistake Script"}</span>
              <br />
              Script 2 must be: <span className="font-semibold">{selectedScripts[0]?.type === "mistake_engagement" ? "Mistake Script" : "Mistake Engagement"}</span>
            </p>
          ) : (
            <p className="text-sm text-blue-700">
              Script 1 selected: <span className="font-semibold">{selectedScripts[0]?.type === "engagement" ? "Engagement Trigger" : "Other Script"}</span>
              <br />
              Script 2 must be: <span className="font-semibold">{selectedScripts[0]?.type === "engagement" ? "Other Script" : "Engagement Trigger"}</span>
            </p>
          )}
        </div>
      )}

      {/* For Script 4, show viral plug label */}
      {currentScriptIndex === 3 && (
        <div className="mb-4 overflow-x-auto pb-1 -mx-1 px-1">
          <TabButton
            active={true}
            onClick={() => {}}
            testId={isMistakeStyle ? "scripts-tab-mistake-viral" : "scripts-tab-viral-plug"}
          >
            {isMistakeStyle ? "Mistake Viral Plug Scripts" : "Viral Plug Scripts"}
          </TabButton>
        </div>
      )}

      {/* For Scripts 3 and 5, show other scripts label */}
      {(currentScriptIndex === 2 || currentScriptIndex === 4) && (
        <div className="mb-4">
          <TabButton
            active={true}
            onClick={() => {}}
            testId={isMistakeStyle ? "scripts-tab-mistake" : "scripts-tab-other"}
          >
            {isMistakeStyle ? "Mistake Scripts" : "Other Scripts"}
          </TabButton>
        </div>
      )}

      {/* Mobile: Card Layout */}
      <div className="md:hidden space-y-2">
        {filteredScripts.map((script) => {
          const isSelected = selectedScripts.some(s => s?.id === script.id);
          const canSelect = canSelectScript(script);
          const disabledReason = getDisabledReason(script);
          
          return (
            <motion.div
              key={script.id}
              whileTap={canSelect ? { scale: 0.98 } : undefined}
              whileHover={{ backgroundColor: canSelect ? 'rgba(255, 120, 112, 0.05)' : undefined }}
              className={`bg-white rounded-xl border border-slate-100 shadow-sm p-3 sm:p-4 cursor-pointer transition-colors ${
                isSelected ? 'bg-emerald-50/50 border-emerald-200 ring-2 ring-emerald-100' : ''
              } ${!canSelect ? 'opacity-40 cursor-not-allowed' : 'active:scale-[0.98]'}`}
              onClick={() => canSelect && onSelect(script, currentScriptIndex)}
              data-testid={`script-${script.id}`}
              title={disabledReason}
            >
              <div className="flex items-start gap-2 sm:gap-3">
                <Checkbox 
                  checked={isSelected}
                  disabled={!canSelect}
                  onCheckedChange={() => canSelect && onSelect(script, currentScriptIndex)}
                  data-testid={`script-checkbox-${script.id}`}
                  className="mt-0.5"
                />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-[#0F172A] mb-1 leading-snug">{script.paragraph1}</p>
                  <p className="text-xs text-slate-600 mb-2 leading-relaxed line-clamp-3">{script.paragraph2}</p>
                  {isSelected ? (
                    <span className="text-emerald-600 text-xs font-medium">Selected</span>
                  ) : disabledReason ? (
                    <span className="text-slate-400 text-xs italic" title={disabledReason}>Unavailable</span>
                  ) : (
                    script.notes && <span className="text-slate-500 text-xs">{script.notes}</span>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
      
      {/* Desktop: Table Layout */}
      <div className="hidden md:block bg-white rounded-2xl border border-slate-100 shadow-xl shadow-slate-200/50 overflow-hidden">
        <div className="grid grid-cols-[60px_80px_200px_1fr_100px] bg-[#0F172A] text-white text-xs font-bold uppercase tracking-wider">
          <div className="px-4 py-3">Select</div>
          <div className="px-4 py-3">Rank</div>
          <div className="px-4 py-3">Paragraph 1</div>
          <div className="px-4 py-3">Paragraph 2</div>
          <div className="px-4 py-3">Notes</div>
        </div>
        
        <div className="divide-y divide-slate-50">
          {filteredScripts.map((script) => {
            const isSelected = selectedScripts.some(s => s?.id === script.id);
            const canSelect = canSelectScript(script);
            const disabledReason = getDisabledReason(script);
            
            return (
              <motion.div
                key={script.id}
                whileHover={{ backgroundColor: canSelect ? 'rgba(255, 120, 112, 0.05)' : undefined }}
                className={`grid grid-cols-[60px_80px_200px_1fr_100px] items-start cursor-pointer transition-colors ${
                  isSelected ? 'bg-emerald-50/50 opacity-50' : ''
                } ${!canSelect ? 'opacity-40 cursor-not-allowed' : ''}`}
                onClick={() => canSelect && onSelect(script, currentScriptIndex)}
                data-testid={`script-${script.id}`}
                title={disabledReason}
              >
                <div className="px-4 py-4 flex justify-center">
                  <Checkbox 
                    checked={isSelected}
                    disabled={!canSelect}
                    onCheckedChange={() => canSelect && onSelect(script, currentScriptIndex)}
                    data-testid={`script-checkbox-${script.id}`}
                  />
                </div>
                <div className="px-4 py-4 text-sm text-slate-500">
                  {script.rank || '-'}
                </div>
                <div className="px-4 py-4 text-sm text-[#0F172A] font-medium">
                  {script.paragraph1}
                </div>
                <div className="px-4 py-4 text-sm text-slate-600">
                  {script.paragraph2}
                </div>
                <div className="px-4 py-4 text-sm text-slate-500">
                  {isSelected ? (
                    <span className="text-emerald-600 font-medium">Selected</span>
                  ) : disabledReason ? (
                    <span className="text-slate-400 italic" title={disabledReason}>Unavailable</span>
                  ) : (
                    script.notes || '-'
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
      
      {/* Selection indicator */}
      {selectedScripts[currentScriptIndex] && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-3 bg-emerald-50 rounded-lg flex items-center gap-2 text-sm"
        >
          <Check className="w-4 h-4 text-emerald-600" />
          <span className="text-emerald-700">Script {currentScriptIndex + 1}: {selectedScripts[currentScriptIndex].paragraph1.substring(0, 40)}...</span>
        </motion.div>
      )}
    </motion.div>
  );
};

// Summary Step - Improved Layout
const SummaryStep = ({ selectedStyle, selectedHook, selectedScripts, onBackToEdit, onImageClick }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <h2 className="text-lg md:text-2xl font-bold text-center mb-2 text-[#0F172A] px-2">Content Summary</h2>
      <p className="text-slate-500 text-center mb-4 md:mb-8 text-sm md:text-base px-4">Review your selections and copy each item for your content creation</p>
      
      <div className="space-y-3 sm:space-y-4 md:space-y-6">
        {/* Visual Style Summary */}
        <div className="bg-white rounded-xl md:rounded-2xl border border-slate-100 shadow-lg p-3 sm:p-4 md:p-6">
          <h3 className="text-[10px] sm:text-xs md:text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2 sm:mb-3 md:mb-4">Visual Style</h3>
          {selectedStyle ? (
            <div>
              <p className="font-semibold text-[#0F172A] mb-2 md:mb-3 text-sm md:text-base">{selectedStyle.title}</p>
              <div className="flex gap-2 md:gap-3 flex-wrap">
                {selectedStyle.images.map((img, idx) => (
                  <img
                    key={idx}
                    src={img}
                    alt={`${selectedStyle.title} preview ${idx + 1}`}
                    className="w-14 h-14 sm:w-16 sm:h-16 md:w-20 md:h-20 object-cover rounded-lg border border-slate-200 cursor-zoom-in hover:border-[#FF7870] hover:shadow-md transition-all"
                    onClick={() => onImageClick(selectedStyle.images.map((imgUrl, i) => ({ 
                      src: imgUrl, 
                      alt: `${selectedStyle.title} preview ${i + 1}` 
                    })))}
                  />
                ))}
              </div>
            </div>
          ) : (
            <p className="text-slate-400 text-sm">No style selected</p>
          )}
        </div>

        {/* Hook Summary */}
        <div className="bg-white rounded-xl md:rounded-2xl border border-slate-100 shadow-lg p-3 sm:p-4 md:p-6">
          <h3 className="text-[10px] sm:text-xs md:text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2 sm:mb-3 md:mb-4">Hook</h3>
          {selectedHook ? (
            <div className="flex items-start justify-between gap-2 md:gap-4">
              <p className="text-[#0F172A] flex-1 text-sm md:text-base">{selectedHook.idea}</p>
              <CopyButton text={selectedHook.idea} label="Hook" />
            </div>
          ) : (
            <p className="text-slate-400 text-sm">No hook selected</p>
          )}
        </div>

        {/* Scripts Summary - Detailed Layout */}
        <div className="bg-white rounded-xl md:rounded-2xl border border-slate-100 shadow-lg p-3 sm:p-4 md:p-6">
          <h3 className="text-[10px] sm:text-xs md:text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3 sm:mb-4 md:mb-6">Scripts</h3>
          <div className="space-y-3 sm:space-y-4 md:space-y-6">
            {selectedScripts.map((script, idx) => (
              <div key={idx} className="border border-slate-100 rounded-lg md:rounded-xl p-2.5 sm:p-3 md:p-5">
                <div className="flex items-center gap-2 md:gap-3 mb-2 sm:mb-3 md:mb-4">
                  <span className="text-sm sm:text-base md:text-lg font-bold text-[#0F172A]">Script {idx + 1}</span>
                  <span className="px-1.5 py-0.5 sm:px-2 sm:py-0.5 md:px-3 md:py-1 bg-[#0F172A] text-white text-[9px] sm:text-[10px] md:text-xs font-medium rounded-full">
                    Position {idx + 1}
                  </span>
                </div>
                
                {script ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-6">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs md:text-sm font-medium text-slate-500">Paragraph 1:</span>
                        <CopyButton text={script.paragraph1} label={`Script ${idx + 1} P1`} />
                      </div>
                      <div className="bg-slate-50 rounded-lg p-3 md:p-4">
                        <p className="text-xs md:text-sm text-[#0F172A]">{script.paragraph1}</p>
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs md:text-sm font-medium text-slate-500">Paragraph 2:</span>
                        <CopyButton text={script.paragraph2} label={`Script ${idx + 1} P2`} />
                      </div>
                      <div className="bg-slate-50 rounded-lg p-3 md:p-4">
                        <p className="text-xs md:text-sm text-[#0F172A]">{script.paragraph2}</p>
                      </div>
                    </div>
                  </div>
                ) : (
                  <p className="text-slate-400 text-xs md:text-sm">Not selected</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Back to Edit Button */}
        <div className="flex justify-center pt-2 md:pt-4">
          <Button
            variant="outline"
            onClick={onBackToEdit}
            className="rounded-full px-4 md:px-8 py-3 md:py-6 font-medium border-slate-200 hover:bg-slate-50 text-sm md:text-base"
            data-testid="back-to-edit-btn"
          >
            <ArrowLeft className="w-4 h-4 mr-1 md:mr-2" />
            Back to Edit
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

// Main Content Creator Component
const ContentCreator = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [visualStyles, setVisualStyles] = useState([]);
  const [hooks, setHooks] = useState([]);
  const [scripts, setScripts] = useState([]);
  const [selectedStyle, setSelectedStyle] = useState(null);
  const [selectedHook, setSelectedHook] = useState(null);
  const [selectedScripts, setSelectedScripts] = useState([undefined, undefined, undefined, undefined, undefined]);
  const [currentScriptIndex, setCurrentScriptIndex] = useState(0);
  const [lastUpdated] = useState(new Date().toLocaleString('de-DE'));
  const [lightboxImage, setLightboxImage] = useState(null);

  const steps = [
    { id: 1, label: "Visual Style", sublabel: "Choose your style" },
    { id: 2, label: "Hook", sublabel: "Select your hook" },
    { id: 3, label: "Scripts", sublabel: "Pick 5 scripts" },
    { id: 4, label: "Summary", sublabel: "Review & copy" }
  ];

  useEffect(() => {
    // Load data from local JSON file
    setVisualStyles(contentData.visualStyles);
    setHooks(contentData.hooks);
    setScripts(contentData.scripts);
  }, []);

  const handleScriptSelect = (script, index, remove = false) => {
    if (remove) {
      const newScripts = [...selectedScripts];
      newScripts[index] = undefined;
      setSelectedScripts(newScripts);
      setCurrentScriptIndex(index);
      return;
    }

    const newScripts = [...selectedScripts];
    newScripts[index] = script;
    setSelectedScripts(newScripts);
    
    // Move to next empty slot
    const nextEmpty = newScripts.findIndex((s, i) => i > index && s === undefined);
    if (nextEmpty !== -1) {
      setCurrentScriptIndex(nextEmpty);
    } else {
      // Find first empty slot
      const firstEmpty = newScripts.findIndex(s => s === undefined);
      if (firstEmpty !== -1) {
        setCurrentScriptIndex(firstEmpty);
      }
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 0: return selectedStyle !== null;
      case 1: return selectedHook !== null;
      case 2: return selectedScripts.filter(s => s !== undefined).length === 5;
      default: return true;
    }
  };

  const handleNext = () => {
    if (canProceed() && currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleBackToEdit = () => {
    setCurrentStep(0);
  };

  return (
    <div className="min-h-screen" data-testid="content-creator">
      <Toaster position="top-right" />
      
      {/* Global Lightbox */}
      {lightboxImage && (
        <ImageLightbox
          images={lightboxImage}
          onClose={() => setLightboxImage(null)}
        />
      )}
      
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50 safe-area-pt">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 py-2.5 sm:py-3 md:py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 md:gap-3">
            <div className="w-7 h-7 md:w-8 md:h-8 bg-[#FF7870] rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-white font-bold text-sm md:text-lg">V</span>
            </div>
            <span className="font-semibold text-[#0F172A] text-sm sm:text-base md:text-lg">She's Viral</span>
          </div>
          <div className="flex items-center gap-2 md:gap-4">
            <button className="flex items-center gap-1 md:gap-2 text-[#FF7870] hover:text-[#E66A63] text-xs md:text-sm font-medium p-1.5 sm:p-2 rounded-lg hover:bg-pink-50 transition-colors" data-testid="sign-out-btn">
              <LogOut className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              <span className="hidden sm:inline">Sign Out</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-3 sm:px-4 md:px-6 py-3 sm:py-4 md:py-8">
        <div className="mb-4 md:mb-8">
          <h1 className="text-xl md:text-3xl font-bold text-[#0F172A]">Content Dashboard</h1>
          <p className="text-slate-500 text-xs md:text-sm">Last updated: {lastUpdated}</p>
        </div>

        {/* Content Creator Card */}
        <div className="bg-white rounded-xl sm:rounded-2xl md:rounded-3xl border border-slate-100 shadow-lg sm:shadow-xl md:shadow-2xl shadow-slate-200/50 p-3 sm:p-4 md:p-8 lg:p-12">
          <h2 className="text-base sm:text-lg md:text-2xl font-bold text-center mb-3 sm:mb-4 md:mb-8 text-[#0F172A]">Content Creator</h2>
          
          <Stepper currentStep={currentStep} steps={steps} />
          
          <AnimatePresence mode="wait">
            {currentStep === 0 && (
              <VisualStyleStep
                key="visual"
                visualStyles={visualStyles}
                selectedStyle={selectedStyle}
                onSelect={setSelectedStyle}
                onImageClick={setLightboxImage}
              />
            )}
            {currentStep === 1 && (
              <HookStep
                key="hook"
                hooks={hooks}
                selectedHook={selectedHook}
                onSelect={setSelectedHook}
                selectedStyle={selectedStyle}
              />
            )}
            {currentStep === 2 && (
              <ScriptStep
                key="scripts"
                scripts={scripts}
                selectedScripts={selectedScripts}
                onSelect={handleScriptSelect}
                currentScriptIndex={currentScriptIndex}
                setCurrentScriptIndex={setCurrentScriptIndex}
                selectedStyle={selectedStyle}
              />
            )}
            {currentStep === 3 && (
              <SummaryStep
                key="summary"
                selectedStyle={selectedStyle}
                selectedHook={selectedHook}
                selectedScripts={selectedScripts}
                onBackToEdit={handleBackToEdit}
                onImageClick={setLightboxImage}
              />
            )}
          </AnimatePresence>
        </div>

        {/* Navigation Buttons - Fixed at bottom */}
        {currentStep < 3 && (
          <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-100 z-50" style={{ paddingBottom: 'max(16px, env(safe-area-inset-bottom, 0px))' }}>
            <div className="max-w-6xl mx-auto px-4 py-4 sm:py-5">
              <div className="flex justify-between gap-3 sm:gap-4">
                <Button
                  variant="outline"
                  onClick={handleBack}
                  disabled={currentStep === 0}
                  className="rounded-full px-6 sm:px-8 font-medium border-slate-200 hover:bg-slate-50 text-sm sm:text-base flex-1 md:flex-none h-12 sm:h-14 touch-manipulation"
                  data-testid="back-btn"
                >
                  <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
                  <span>Back</span>
                </Button>
                
                <Button
                  onClick={handleNext}
                  disabled={!canProceed()}
                  className={`rounded-full px-6 sm:px-8 font-medium text-sm sm:text-base flex-1 md:flex-none h-12 sm:h-14 touch-manipulation ${
                    canProceed() 
                      ? 'bg-[#FF7870] hover:bg-[#E66A63] text-white shadow-lg shadow-pink-200' 
                      : 'bg-slate-100 text-slate-400'
                  }`}
                  data-testid="next-btn"
                >
                  <span>Next</span>
                  <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 ml-2" />
                </Button>
              </div>
            </div>
          </div>
        )}
        
        {/* Spacer for fixed navigation */}
        {currentStep < 3 && <div className="h-24 sm:h-28 md:h-32"></div>}
      </main>
    </div>
  );
};

function App() {
  return <ContentCreator />;
}

export default App;
