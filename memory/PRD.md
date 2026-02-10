# Social Media Content Creator - PRD

## Original Problem Statement
"Mach mir die webseite" - Build a Social Media Content Creator dashboard based on provided screenshots showing a 4-step content creation wizard.

## User Personas
- **Content Creators**: TikTok/Social Media creators looking for content templates
- **Social Media Managers**: Professionals managing multiple accounts

## Core Requirements (Static)
1. 4-step wizard workflow
2. Visual Style selection with image previews
3. Hook selection with category tabs
4. Script selection (5 scripts with rules)
5. Summary page with copy functionality
6. No authentication required
7. Dummy data for MVP

## What's Been Implemented (9.2.2026)
- ✅ Backend API with dummy data (/api/visual-styles, /api/hooks, /api/scripts)
- ✅ Visual Style step with 12 style options and image previews
- ✅ Hook step with 5 category tabs (Ex TikTok, Professor, Official TikTok, Experienced, Learnings)
- ✅ Scripts step with 3 types: Other Scripts, Engagement Triggers, Viral Plug Scripts
- ✅ Script 4 automatically enforces Viral Plug Scripts requirement
- ✅ Script Selection Progress with Remove links for each script
- ✅ Summary step with detailed layout - Position badges, Paragraph 1/2 with individual Copy buttons
- ✅ Back to Edit button on Summary page
- ✅ Responsive stepper navigation
- ✅ Coral/pink themed design per screenshots

## Prioritized Backlog

### P0 (Critical)
- None - MVP complete

### P1 (High)
- User authentication (login/register)
- Save generated content to database
- Content history/versioning

### P2 (Medium)
- Export content as PDF/image
- Custom hook/script creation
- Team collaboration features

### P3 (Nice to Have)
- AI-powered script suggestions
- Analytics dashboard
- Template marketplace

## Next Tasks
1. Add user authentication
2. Implement content saving functionality
3. Add content history page
