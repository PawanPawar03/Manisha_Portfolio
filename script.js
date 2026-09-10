/**
 * MANISHA AVINASH PATKE - DYNAMIC PORTFOLIO INTERACTIVE JAVASCRIPT
 * Professional, Fast & Responsive Interactions
 */

document.addEventListener('DOMContentLoaded', () => {

  /* ----------------------------------------------------
     1. THEME TOGGLE (DARK / LIGHT MODE)
  ---------------------------------------------------- */
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const htmlRoot = document.documentElement;

  // Retrieve saved preference or default to dark
  const savedTheme = localStorage.getItem('manisha_portfolio_theme') || 'dark';
  htmlRoot.setAttribute('data-theme', savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = htmlRoot.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      htmlRoot.setAttribute('data-theme', newTheme);
      localStorage.setItem('manisha_portfolio_theme', newTheme);
      showToast(`Switched to ${newTheme === 'dark' ? 'Dark' : 'Light'} Mode`, 'info');
    });
  }

  /* ----------------------------------------------------
     2. NAVBAR SCROLL & ACTIVE SECTION HIGHLIGHT
  ---------------------------------------------------- */
  const navbar = document.getElementById('navbar');
  const scrollProgress = document.getElementById('scroll-progress');
  const backToTopBtn = document.getElementById('back-to-top');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPct = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;

    // Update top progress bar
    if (scrollProgress) {
      scrollProgress.style.width = `${scrollPct}%`;
    }

    // Navbar style on scroll
    if (navbar) {
      if (scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }

    // Back to top button visibility
    if (backToTopBtn) {
      if (scrollY > 400) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }

    // Highlight active section nav link
    let currentSectionId = '';
    sections.forEach(sec => {
      const secTop = sec.offsetTop - 140;
      const secHeight = sec.offsetHeight;
      if (scrollY >= secTop && scrollY < secTop + secHeight) {
        currentSectionId = sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSectionId}`) {
        link.classList.add('active');
      }
    });
  });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ----------------------------------------------------
     3. MOBILE NAVIGATION MENU
  ---------------------------------------------------- */
  const menuToggle = document.getElementById('menu-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navCloseBtn = document.getElementById('nav-close-btn');
  const navOverlay = document.getElementById('nav-overlay');

  function openMobileMenu() {
    if (menuToggle) menuToggle.classList.add('active');
    if (navMenu) navMenu.classList.add('active');
    if (navOverlay) navOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
  }

  function closeMobileMenu() {
    if (menuToggle) menuToggle.classList.remove('active');
    if (navMenu) navMenu.classList.remove('active');
    if (navOverlay) navOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (menuToggle) {
    menuToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (navMenu && navMenu.classList.contains('active')) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });
  }

  if (navCloseBtn) {
    navCloseBtn.addEventListener('click', closeMobileMenu);
  }

  if (navOverlay) {
    navOverlay.addEventListener('click', closeMobileMenu);
  }

  // Close menu when clicking link
  navLinks.forEach(link => {
    link.addEventListener('click', closeMobileMenu);
  });

  // Close when pressing Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu && navMenu.classList.contains('active')) {
      closeMobileMenu();
    }
  });

  /* ----------------------------------------------------
     4. DYNAMIC TYPEWRITER EFFECT
  ---------------------------------------------------- */
  const typewriterElement = document.getElementById('typewriter');
  if (typewriterElement) {
    const roles = [
      'Accounting & Tally Prime Specialist',
      'Advanced Excel & Data Analyst',
      'Office Operations & Administration Executive',
      'Bilingual Typing & Records Expert (40 WPM)'
    ];

    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 90;

    function type() {
      const currentRole = roles[roleIndex];

      if (isDeleting) {
        typewriterElement.textContent = currentRole.substring(0, charIndex - 1);
        charIndex--;
        typingSpeed = 45;
      } else {
        typewriterElement.textContent = currentRole.substring(0, charIndex + 1);
        charIndex++;
        typingSpeed = 90;
      }

      if (!isDeleting && charIndex === currentRole.length) {
        typingSpeed = 1800; // Pause at end of word
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        typingSpeed = 400; // Pause before new word
      }

      setTimeout(type, typingSpeed);
    }

    type();
  }

  /* ----------------------------------------------------
     5. HERO STATS COUNTER ANIMATION
  ---------------------------------------------------- */
  const counters = document.querySelectorAll('.counter');
  let countersStarted = false;

  function runCounters() {
    counters.forEach(counter => {
      const target = +counter.getAttribute('data-target');
      let count = 0;
      const increment = Math.ceil(target / 40);

      const updateCount = () => {
        count += increment;
        if (count < target) {
          counter.textContent = count;
          setTimeout(updateCount, 35);
        } else {
          counter.textContent = target;
        }
      };
      updateCount();
    });
  }

  // Trigger counters when hero comes into view
  const heroSection = document.getElementById('home');
  if (heroSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !countersStarted) {
          countersStarted = true;
          runCounters();
        }
      });
    }, { threshold: 0.2 });
    observer.observe(heroSection);
  }

  /* ----------------------------------------------------
     6. PARTICLES CANVAS ANIMATION
  ---------------------------------------------------- */
  const canvas = document.getElementById('particles-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particlesArray = [];
    let w, h;

    function resizeCanvas() {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    class Particle {
      constructor() {
        this.x = Math.random() * w;
        this.y = Math.random() * h;
        this.size = Math.random() * 2 + 1;
        this.speedX = (Math.random() - 0.5) * 0.6;
        this.speedY = (Math.random() - 0.5) * 0.6;
        this.color = Math.random() > 0.5 ? 'rgba(99, 102, 241, 0.4)' : 'rgba(6, 182, 212, 0.35)';
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.x > w) this.x = 0;
        if (this.x < 0) this.x = w;
        if (this.y > h) this.y = 0;
        if (this.y < 0) this.y = h;
      }
      draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function initParticles() {
      particlesArray = [];
      const numberOfParticles = Math.min(Math.floor((w * h) / 18000), 65);
      for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
      }
    }
    initParticles();

    function animateParticles() {
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();

        // Connect nearby particles
        for (let j = i + 1; j < particlesArray.length; j++) {
          const dx = particlesArray[i].x - particlesArray[j].x;
          const dy = particlesArray[i].y - particlesArray[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 100) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(99, 102, 241, ${0.15 - dist / 700})`;
            ctx.lineWidth = 0.6;
            ctx.moveTo(particlesArray[i].x, particlesArray[i].y);
            ctx.lineTo(particlesArray[j].x, particlesArray[j].y);
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(animateParticles);
    }
    animateParticles();
  }

  /* ----------------------------------------------------
     7. SKILLS FILTERING & PROGRESS ANIMATION
  ---------------------------------------------------- */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const skillCards = document.querySelectorAll('.skill-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      skillCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'block';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          }, 20);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.96)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 200);
        }
      });
    });
  });

  // Animate skill progress bars on scroll
  const skillSection = document.getElementById('skills');
  if (skillSection) {
    const skillObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          document.querySelectorAll('.skill-fill').forEach(bar => {
            bar.classList.add('animated');
          });
        }
      });
    }, { threshold: 0.2 });
    skillObserver.observe(skillSection);
  }

  /* ----------------------------------------------------
     8. SIMULATOR NAVIGATION TABS
  ---------------------------------------------------- */
  const simTabBtns = document.querySelectorAll('.sim-tab-btn');
  const simPanels = document.querySelectorAll('.sim-panel');

  simTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetSim = btn.getAttribute('data-sim');

      simTabBtns.forEach(b => b.classList.remove('active'));
      simPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPanel = document.getElementById(`sim-${targetSim}`);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });

  /* ----------------------------------------------------
     9. SIMULATOR TAB 1: GST & INVOICE VOUCHER CALCULATOR
  ---------------------------------------------------- */
  const invClient = document.getElementById('inv-client');
  const invItem = document.getElementById('inv-item');
  const invQty = document.getElementById('inv-qty');
  const invRate = document.getElementById('inv-rate');
  const invGst = document.getElementById('inv-gst');

  const resClient = document.getElementById('res-client');
  const resItem = document.getElementById('res-item');
  const resQty = document.getElementById('res-qty');
  const resRate = document.getElementById('res-rate');
  const resSubtotal = document.getElementById('res-subtotal');
  const taxSubtotal = document.getElementById('tax-subtotal');
  const cgstRate = document.getElementById('cgst-rate');
  const cgstAmount = document.getElementById('cgst-amount');
  const sgstRate = document.getElementById('sgst-rate');
  const sgstAmount = document.getElementById('sgst-amount');
  const grandTotal = document.getElementById('grand-total');

  function calculateVoucher() {
    const client = invClient.value.trim() || 'Valued Client';
    const item = invItem.value.trim() || 'Services Rendered';
    const qty = Math.max(1, parseFloat(invQty.value) || 1);
    const rate = Math.max(0, parseFloat(invRate.value) || 0);
    const totalGstPercent = parseFloat(invGst.value) || 0;

    const subtotalVal = qty * rate;
    const halfGstPercent = totalGstPercent / 2;
    const halfTaxAmount = (subtotalVal * halfGstPercent) / 100;
    const totalVal = subtotalVal + (halfTaxAmount * 2);

    // Format Currency Helper (INR)
    const formatINR = (val) => '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    resClient.textContent = client;
    resItem.textContent = item;
    resQty.textContent = qty;
    resRate.textContent = formatINR(rate);
    resSubtotal.textContent = formatINR(subtotalVal);
    taxSubtotal.textContent = formatINR(subtotalVal);

    cgstRate.textContent = halfGstPercent;
    cgstAmount.textContent = formatINR(halfTaxAmount);
    sgstRate.textContent = halfGstPercent;
    sgstAmount.textContent = formatINR(halfTaxAmount);

    grandTotal.textContent = formatINR(totalVal);
  }

  // Bind live calculation listeners
  [invClient, invItem, invQty, invRate, invGst].forEach(el => {
    if (el) {
      el.addEventListener('input', calculateVoucher);
      el.addEventListener('change', calculateVoucher);
    }
  });

  const recalculateBtn = document.getElementById('calc-recalculate-btn');
  if (recalculateBtn) {
    recalculateBtn.addEventListener('click', () => {
      calculateVoucher();
      showToast('Voucher recalculated successfully!', 'success');
    });
  }

  const resetVoucherBtn = document.getElementById('calc-reset-btn');
  if (resetVoucherBtn) {
    resetVoucherBtn.addEventListener('click', () => {
      invClient.value = 'Apex Enterprises Nanded';
      invItem.value = 'Accounting & Audit Services';
      invQty.value = '2';
      invRate.value = '12500';
      invGst.value = '18';
      calculateVoucher();
      showToast('Voucher inputs reset to default', 'info');
    });
  }

  // Initial calculation
  calculateVoucher();

  /* ----------------------------------------------------
     10. SIMULATOR TAB 2: INTERACTIVE EXCEL TABLE
  ---------------------------------------------------- */
  const initialExcelData = [
    { voucher: 'VCH-1001', head: 'Sales of Software Services', cat: 'Income', debit: 0, credit: 85000, status: 'Posted' },
    { voucher: 'VCH-1002', head: 'Office Rent & Facilities', cat: 'Expense', debit: 25000, credit: 0, status: 'Audited' },
    { voucher: 'VCH-1003', head: 'Computer & Hardware Equipment', cat: 'Asset', debit: 45000, credit: 0, status: 'Verified' },
    { voucher: 'VCH-1004', head: 'GST Output Tax Payable', cat: 'Tax', debit: 0, credit: 15300, status: 'Pending' },
    { voucher: 'VCH-1005', head: 'Accounting & Consultation Fees', cat: 'Income', debit: 0, credit: 74200, status: 'Posted' },
    { voucher: 'VCH-1006', head: 'Stationery & Operational Supplies', cat: 'Expense', debit: 8500, credit: 0, status: 'Audited' },
    { voucher: 'VCH-1007', head: 'Bank Balance (SBI Current A/c)', cat: 'Asset', debit: 96000, credit: 0, status: 'Reconciled' }
  ];

  const excelTbody = document.getElementById('excel-tbody');
  const excelSearch = document.getElementById('excel-search');
  const excelFilterCat = document.getElementById('excel-filter-cat');
  const xlCount = document.getElementById('xl-count');
  const xlSumDebit = document.getElementById('xl-sum-debit');
  const xlSumCredit = document.getElementById('xl-sum-credit');
  const xlBalanceStatus = document.getElementById('xl-balance-status');

  function renderExcelTable() {
    if (!excelTbody) return;

    const searchTerm = (excelSearch ? excelSearch.value : '').toLowerCase().trim();
    const catFilter = excelFilterCat ? excelFilterCat.value : 'all';

    const filtered = initialExcelData.filter(row => {
      const matchSearch = row.head.toLowerCase().includes(searchTerm) || row.voucher.toLowerCase().includes(searchTerm);
      const matchCat = catFilter === 'all' || row.cat === catFilter;
      return matchSearch && matchCat;
    });

    excelTbody.innerHTML = '';
    let totalDebit = 0;
    let totalCredit = 0;

    if (filtered.length === 0) {
      excelTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No matching ledger records found.</td></tr>`;
    } else {
      filtered.forEach(item => {
        totalDebit += item.debit;
        totalCredit += item.credit;

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${item.voucher}</strong></td>
          <td>${item.head}</td>
          <td><span class="tag">${item.cat}</span></td>
          <td style="color: ${item.debit > 0 ? '#38bdf8' : 'inherit'}">${item.debit > 0 ? '₹' + item.debit.toLocaleString('en-IN') : '-'}</td>
          <td style="color: ${item.credit > 0 ? '#34d399' : 'inherit'}">${item.credit > 0 ? '₹' + item.credit.toLocaleString('en-IN') : '-'}</td>
          <td><span class="status-green"><i class="fa-solid fa-circle-check"></i> ${item.status}</span></td>
        `;
        excelTbody.appendChild(tr);
      });
    }

    if (xlCount) xlCount.textContent = filtered.length;
    if (xlSumDebit) xlSumDebit.textContent = '₹' + totalDebit.toLocaleString('en-IN');
    if (xlSumCredit) xlSumCredit.textContent = '₹' + totalCredit.toLocaleString('en-IN');

    if (xlBalanceStatus) {
      if (totalDebit === totalCredit) {
        xlBalanceStatus.innerHTML = '<i class="fa-solid fa-check"></i> Balanced';
        xlBalanceStatus.className = 'val text-accent';
      } else {
        xlBalanceStatus.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Filtered View';
        xlBalanceStatus.className = 'val text-orange';
      }
    }
  }

  if (excelSearch) excelSearch.addEventListener('input', renderExcelTable);
  if (excelFilterCat) excelFilterCat.addEventListener('change', renderExcelTable);
  renderExcelTable();

  /* ----------------------------------------------------
     11. SIMULATOR TAB 3: TYPING SPEED TESTER
  ---------------------------------------------------- */
  const quoteDisplay = document.getElementById('quote-display');
  const typingInput = document.getElementById('typing-input');
  const startTypingBtn = document.getElementById('start-typing-btn');
  const resetTypingBtn = document.getElementById('reset-typing-btn');
  const typeTimer = document.getElementById('type-timer');
  const typeWpm = document.getElementById('type-wpm');
  const typeAcc = document.getElementById('type-acc');

  const sampleQuote = "Accounting precision, ledger reconciliation, and advanced data modeling in spreadsheets are foundational skills for modern financial management and administrative operations.";
  let timerInterval = null;
  let timeLeft = 30;
  let testActive = false;
  let totalCharactersTyped = 0;

  function setupQuote() {
    if (!quoteDisplay) return;
    quoteDisplay.innerHTML = '';
    sampleQuote.split('').forEach((char, index) => {
      const span = document.createElement('span');
      span.innerText = char;
      span.classList.add('quote-char');
      if (index === 0) span.classList.add('current');
      quoteDisplay.appendChild(span);
    });
  }
  setupQuote();

  function startTypingTest() {
    if (testActive) return;
    testActive = true;
    timeLeft = 30;
    totalCharactersTyped = 0;
    typingInput.value = '';
    typingInput.disabled = false;
    typingInput.focus();
    startTypingBtn.disabled = true;
    startTypingBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Test In Progress';

    setupQuote();

    timerInterval = setInterval(() => {
      timeLeft--;
      typeTimer.textContent = `${timeLeft}s`;

      if (timeLeft <= 0) {
        endTypingTest();
      }
    }, 1000);
  }

  function endTypingTest() {
    clearInterval(timerInterval);
    testActive = false;
    typingInput.disabled = true;
    startTypingBtn.disabled = false;
    startTypingBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start Typing Test';
    showToast(`Test Complete! Speed: ${typeWpm.textContent}, Accuracy: ${typeAcc.textContent}`, 'success');
  }

  function resetTypingTest() {
    clearInterval(timerInterval);
    testActive = false;
    timeLeft = 30;
    typeTimer.textContent = '30s';
    typeWpm.textContent = '0 WPM';
    typeAcc.textContent = '100%';
    typingInput.value = '';
    typingInput.disabled = true;
    startTypingBtn.disabled = false;
    startTypingBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start Typing Test';
    setupQuote();
  }

  if (startTypingBtn) startTypingBtn.addEventListener('click', startTypingTest);
  if (resetTypingBtn) resetTypingBtn.addEventListener('click', resetTypingTest);

  if (typingInput) {
    typingInput.addEventListener('input', () => {
      if (!testActive) return;

      const inputChars = typingInput.value.split('');
      const quoteSpans = quoteDisplay.querySelectorAll('.quote-char');
      let correctChars = 0;

      quoteSpans.forEach((charSpan, index) => {
        const char = inputChars[index];

        charSpan.classList.remove('current');

        if (char == null) {
          charSpan.classList.remove('correct', 'incorrect');
        } else if (char === charSpan.innerText) {
          charSpan.classList.add('correct');
          charSpan.classList.remove('incorrect');
          correctChars++;
        } else {
          charSpan.classList.add('incorrect');
          charSpan.classList.remove('correct');
        }

        if (index === inputChars.length) {
          charSpan.classList.add('current');
        }
      });

      // Calculate WPM and Accuracy
      const timeElapsed = Math.max(1, 30 - timeLeft);
      const minutes = timeElapsed / 60;
      const wpm = Math.round((inputChars.length / 5) / minutes);
      const accuracy = inputChars.length > 0 ? Math.round((correctChars / inputChars.length) * 100) : 100;

      typeWpm.textContent = `${Math.max(0, wpm)} WPM`;
      typeAcc.textContent = `${accuracy}%`;

      // Finish if all characters typed
      if (inputChars.length >= sampleQuote.length) {
        endTypingTest();
      }
    });
  }

  /* ----------------------------------------------------
     12. PRINT RESUME ACTION
  ---------------------------------------------------- */
  const printResumeBtn = document.getElementById('print-resume-btn');
  if (printResumeBtn) {
    printResumeBtn.addEventListener('click', () => {
      window.print();
    });
  }

  /* ----------------------------------------------------
     13. COPY TO CLIPBOARD FUNCTIONALITY
  ---------------------------------------------------- */
  const copyElements = document.querySelectorAll('[data-copy]');
  copyElements.forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const textToCopy = el.getAttribute('data-copy');
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showToast(`Copied to clipboard: ${textToCopy}`, 'success');
        }).catch(() => {
          showToast('Failed to copy. Please copy manually.', 'error');
        });
      }
    });
  });

  /* ----------------------------------------------------
     14. CONTACT FORM VALIDATION & SUBMISSION
  ---------------------------------------------------- */
  const contactForm = document.getElementById('contact-form');
  const successBanner = document.getElementById('form-success-banner');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('contact-name').value.trim();
      const email = document.getElementById('contact-email').value.trim();
      const subject = document.getElementById('contact-subject').value.trim();
      const message = document.getElementById('contact-message').value.trim();
      const phone = document.getElementById('contact-phone').value.trim();

      let hasError = false;

      // Reset errors
      document.getElementById('err-name').textContent = '';
      document.getElementById('err-email').textContent = '';
      document.getElementById('err-subject').textContent = '';
      document.getElementById('err-message').textContent = '';

      if (!name) {
        document.getElementById('err-name').textContent = 'Please enter your full name.';
        hasError = true;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email || !emailPattern.test(email)) {
        document.getElementById('err-email').textContent = 'Please enter a valid email address.';
        hasError = true;
      }

      if (!subject) {
        document.getElementById('err-subject').textContent = 'Please specify a subject.';
        hasError = true;
      }

      if (!message || message.length < 5) {
        document.getElementById('err-message').textContent = 'Please write a message (at least 5 characters).';
        hasError = true;
      }

      if (hasError) return;

      // Simulated submission & persistence to localStorage
      const submission = {
        name,
        email,
        phone,
        subject,
        message,
        timestamp: new Date().toISOString()
      };

      try {
        const storedMessages = JSON.parse(localStorage.getItem('manisha_portfolio_inquiries') || '[]');
        storedMessages.push(submission);
        localStorage.setItem('manisha_portfolio_inquiries', JSON.stringify(storedMessages));
      } catch (err) {
        console.warn('Storage warning', err);
      }

      // Show success
      contactForm.reset();
      if (successBanner) successBanner.style.display = 'flex';
      showToast('Message sent! Manisha will reply soon.', 'success');

      // Scroll to banner
      successBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }

  /* ----------------------------------------------------
     15. TOAST NOTIFICATION HELPER
  ---------------------------------------------------- */
  function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = 'toast';

    let icon = '<i class="fa-solid fa-circle-info text-blue"></i>';
    if (type === 'success') icon = '<i class="fa-solid fa-circle-check text-green"></i>';
    if (type === 'error') icon = '<i class="fa-solid fa-circle-exclamation text-red"></i>';

    toast.innerHTML = `${icon} <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3200);
  }

  // Update current copyright year dynamically
  const currentYearSpan = document.getElementById('current-year');
  if (currentYearSpan) {
    currentYearSpan.textContent = new Date().getFullYear();
  }

});
