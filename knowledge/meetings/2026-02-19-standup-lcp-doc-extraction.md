# Standup - LCP Doc Extraction
**Date:** 2026-02-19 | **Attendees:** 
## Copilot Summary
```json
{
  "meeting_id": "MSplMzNhOGJlMC0wODRlLTQ0MWItODRjNy1hZWI2NzFlYmIzYmIqMCoqMTk6bWVldGluZ19OakEwTURjeVltWXROekk1WVMwMFptSXdMVGxrWkRZdFl6WmtZMlUwTlRRNFltRTBAdGhyZWFkLnYy",
  "join_url": null,
  "has_copilot_insights": true,
  "has_transcript": false,
  "action_items": [
    {
      "title": "Test Account Provisioning and Instructions",
      "text": "Provide Vijay with a test account and necessary files, and explain the steps required for local plugin testing.",
      "owner": "Ajay"
    },
    {
      "title": "Manifest File Troubleshooting and Sharing",
      "text": "Investigate and update the manifest file, then send the updated file to Charlie and Vijay for further testing.",
      "owner": "Ajay"
    },
    {
      "title": "Dashboard Screen Layout Improvement",
      "text": "Modify the dashboard screen layout to improve PDF display by adding three fields and decreasing the size.",
      "owner": "Ajay"
    },
    {
      "title": "Plugin Deployment for Demo",
      "text": "Deploy the plugin to the client tenant by Monday evening IST to enable testing and demo.",
      "owner": "Ajay"
    },
    {
      "title": "Demo Scheduling",
      "text": "Find and schedule a demo slot after 6:00 PM IST on Monday to accommodate plugin deployment timing.",
      "owner": "Navsheen"
    },
    {
      "title": "Testing Priority Communication",
      "text": "Test the AI extraction functionality as the top priority and report any issues encountered.",
      "owner": "Vijay"
    },
    {
      "title": "Document Sharing for Testing",
      "text": "Send the required documents to Vijay via email for testing purposes.",
      "owner": "Navsheen"
    },
    {
      "title": "Manifest File Customization and Feedback",
      "text": "Make customizations to the manifest file and inform the team if the issue is resolved.",
      "owner": "Charlie"
    }
  ],
  "meeting_notes": [
    {
      "title": "Plugin Testing and Deployment Preparation",
      "text": "Ajay explained the current status of the plugin, provided Vijay with instructions and a test account for local testing, and discussed deployment constraints and next steps with Charlie and the team.",
      "subpoints": [
        {
          "title": "Test Account Setup",
          "text": "Ajay informed Vijay that since the plugin is not yet available in their tenant, he would provide Vijay with an account in his own tenant for testing, and outlined the steps Vijay needs to perform locally to test the plugin."
        },
        {
          "title": "Manifest File Issues",
          "text": "Ajay described problems with the manifest file not updating correctly, noted that local testing is disabled in their tenant, and discussed with Charlie the need to side-load the plugin and share the manifest file for troubleshooting."
        },
        {
          "title": "Deployment Constraints",
          "text": "Ajay clarified that his subscription had expired, preventing plugin use in his tenant, and explained to Charlie and Vijay that local testing is also disabled in their Synapse tenant, necessitating alternative arrangements for testing."
        },
        {
          "title": "Deployment Timeline",
          "text": "Ajay stated he would deploy the plugin to the tenant on Monday evening IST, not Monday morning, and coordinated with Navsheen to schedule the onboarding and demo accordingly, while also noting possible risks if issues arise during deployment to the client cloud or Azure services."
        }
      ]
    },
    {
      "title": "Dashboard and Email Ingestion Functionality",
      "text": "Ajay demonstrated the dashboard screen and email ingestion features, detailing how users can upload documents, extract fields, and interact with extracted data, while addressing questions from Vijay and Navsheen.",
      "subpoints": [
        {
          "title": "Dashboard Overview",
          "text": "Ajay presented the dashboard screen, highlighting the display of instrument names, view and edit icons, recent activities, and the method for identifying top issues using a specific field in the request table."
        },
        {
          "title": "Email Ingestion Process",
          "text": "Ajay explained that users can ingest emails or upload documents via the website's email queue, specifying that only PDF uploads are currently enabled, and described how the system extracts fields from uploaded documents."
        },
        {
          "title": "Field Extraction and Selection",
          "text": "Ajay detailed the extraction process, noting that when multiple documents are uploaded, the system selects the value with the highest precision, but users can manually select alternative values if needed."
        },
        {
          "title": "Audit Trail and Field History",
          "text": "Ajay demonstrated that after saving changes, users can view an audit history for each field, including which pages the extracted values came from, and can navigate to and highlight the relevant document pages."
        },
        {
          "title": "Screen Editing and Publishing",
          "text": "Ajay described the workflow for editing and publishing requests, including the requirements for mandatory fields, the ability to edit after publishing, and the options to cancel or discard changes."
        }
      ]
    },
    {
      "title": "Testing Priorities and Demo Planning",
      "text": "Navsheen, Jake, and Vijay discussed testing priorities, emphasizing the importance of AI extraction, and coordinated demo and onboarding schedules based on deployment readiness.",
      "subpoints": [
        {
          "title": "Testing Focus",
          "text": "Jake instructed Vijay to prioritize testing the extraction functionality, stating that it is critical for the application's value, while Navsheen reiterated that basic business requirements must be met before showcasing additional features like the dashboard."
        },
        {
          "title": "Demo and Onboarding Scheduling",
          "text": "Navsheen and Ajay agreed to schedule the onboarding and demo for Monday evening IST, with flexibility to move to Tuesday if deployment issues arise, and Navsheen committed to finding a suitable calendar slot."
        },
        {
          "title": "Contingency Planning",
          "text": "Jake and Ajay discussed the possibility of demoing in their own tenant if deployment to the client tenant is delayed, with Jake expressing willingness to adjust plans to avoid rushing and to ensure a successful demonstration."
        },
        {
          "title": "Document Sharing for Testing",
          "text": "Navsheen confirmed sending necessary documents to Vijay for testing, and Ajay committed to sending additional files within 10-15 minutes to support the testing process."
        }
      ]
    },
    {
      "title": "Technical Deployment Process Discussion",
      "text": "Jake questioned Ajay about the technical process for building and deploying the container to Azure, leading to a detailed explanation of the current Python-based deployment method and suggestions for future improvements.",
      "subpoints": [
        {
          "title": "Current Deployment Method",
          "text": "Ajay explained that, lacking Docker, he uses a Python script with Azure modules to build and deploy the application, specifying tenant, subscription ID, and container names, and deploying directly to Azure BLOB storage and container instances."
        },
        {
          "title": "Suggestions for Improvement",
          "text": "Jake recommended using GitHub runners or similar tools to build Docker images for container apps in the future, suggesting this would be a more standard and maintainable approach."
        }
      ]
    }
  ],
  "transcript_preview": "",
  "error": null,
  "subject": "Standup - LCP Doc Extraction",
  "found_in_calendar": true,
  "organizer_email": "navsheen.koul@synapx.com",
  "organizer_id": null,
  "formatted_summary": "**Action Items:**\n- **Ajay**: Test Account Provisioning and Instructions\n- **Ajay**: Manifest File Troubleshooting and Sharing\n- **Ajay**: Dashboard Screen Layout Improvement\n- **Ajay**: Plugin Deployment for Demo\n- **Navsheen**: Demo Scheduling\n- **Vijay**: Testing Priority Communication\n- **Navsheen**: Document Sharing for Testing\n- **Charlie**: Manifest File Customization and Feedback\n\n**Meeting Notes:**\n\n### Plugin Testing and Deployment Preparation\nAjay explained the current status of the plugin, provided Vijay with instructions and a test account for local testing, and discussed deployment constraints and next steps with Charlie and the team.\n  - **Test Account Setup**: Ajay informed Vijay that since the plugin is not yet available in their tenant, he would provide Vijay with an account in his own tenant for testing, and outlined the steps Vijay needs to perform locally to test the plugin.\n  - **Manifest File Issues**: Ajay described problems with the manifest file not updating correctly, noted that local testing is disabled in their tenant, and discussed with Charlie the need to side-load the plugin and share the manifest file for troubleshooting.\n  - **Deployment Constraints**: Ajay clarified that his subscription had expired, preventing plugin use in his tenant, and explained to Charlie and Vijay that local testing is also disabled in their Synapse tenant, necessitating alternative arrangements for testing.\n  - **Deployment Timeline**: Ajay stated he would deploy the plugin to the tenant on Monday evening IST, not Monday morning, and coordinated with Navsheen to schedule the onboarding and demo accordingly, while also noting possible risks if issues arise during deployment to the client cloud or Azure services.\n\n### Dashboard and Email Ingestion Functionality\nAjay demonstrated the dashboard screen and email ingestion features, detailing how users can upload documents, extract fields, and interact with extracted data, while addressing questions from Vijay and Navsheen.\n  - **Dashboard Overview**: Ajay presented the dashboard screen, highlighting the display of instrument names, view and edit icons, recent activities, and the method for identifying top issues using a specific field in the request table.\n  - **Email Ingestion Process**: Ajay explained that users can ingest emails or upload documents via the website's email queue, specifying that only PDF uploads are currently enabled, and described how the system extracts fields from uploaded documents.\n  - **Field Extraction and Selection**: Ajay detailed the extraction process, noting that when multiple documents are uploaded, the system selects the value with the highest precision, but users can manually select alternative values if needed.\n  - **Audit Trail and Field History**: Ajay demonstrated that after saving changes, users can view an audit history for each field, including which pages the extracted values came from, and can navigate to and highlight the relevant document pages.\n  - **Screen Editing and Publishing**: Ajay described the workflow for editing and publishing requests, including the requirements for mandatory fields, the ability to edit after publishing, and the options to cancel or discard changes.\n\n### Testing Priorities and Demo Planning\nNavsheen, Jake, and Vijay discussed testing priorities, emphasizing the importance of AI extraction, and coordinated demo and onboarding schedules based on deployment readiness.\n  - **Testing Focus**: Jake instructed Vijay to prioritize testing the extraction functionality, stating that it is critical for the application's value, while Navsheen reiterated that basic business requirements must be met before showcasing additional features like the dashboard.\n  - **Demo and Onboarding Scheduling**: Navsheen and Ajay agreed to schedule the onboarding and demo for Monday evening IST, with flexibility to move to Tuesday if deployment issues arise, and Navsheen committed to finding a suitable calendar slot.\n  - **Contingency Planning**: Jake and Ajay discussed the possibility of demoing in their own tenant if deployment to the client tenant is delayed, with Jake expressing willingness to adjust plans to avoid rushing and to ensure a successful demonstration.\n  - **Document Sharing for Testing**: Navsheen confirmed sending necessary documents to Vijay for testing, and Ajay committed to sending additional files within 10-15 minutes to support the testing process.\n\n### Technical Deployment Process Discussion\nJake questioned Ajay about the technical process for building and deploying the container to Azure, leading to a detailed explanation of the current Python-based deployment method and suggestions for future improvements.\n  - **Current Deployment Method**: Ajay explained that, lacking Docker, he uses a Python script with Azure modules to build and deploy the application, specifying tenant, subscription ID, and container names, and deploying directly to Azure BLOB storage and container instances.\n  - **Suggestions for Improvement**: Jake recommended using GitHub runners or similar tools to build Docker images for container apps in the future, suggesting this would be a more standard and maintainable approach."
}
```
## Transcript Preview

