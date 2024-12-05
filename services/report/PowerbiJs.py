from playwright.sync_api import sync_playwright
from datetime import datetime
from core.models.report.ResultModel import Result
from services.report.VisualFormatting import formatData
from constant.Constant import embedURL
import json

def visualExtraction(embedToken, reportId, workspaceId, pageName, slicerOptions=[]):
    try:

        slicerListLength = len(slicerOptions) if slicerOptions else 0

        embedUrl = embedURL.format(reportId=reportId, workspaceId=workspaceId)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            page = context.new_page()

            page.evaluate("""
                var script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/powerbi-client/2.15.1/powerbi.min.js';
                document.head.appendChild(script);
            """)

            page.wait_for_function("typeof window['powerbi-client'] !== 'undefined';")

            if slicerListLength > 0:
                slicerContent = ""
                for slicer in slicerOptions:
                    slicerContent += f"""
                        if ((visual.type === "slicer" || visual.type === "advancedSlicerVisual") && visual.name === "{slicer.SlicerId}") {{
                            const slicerState = await visual.getSlicerState();
                            const tableName = slicerState.targets[0].table;
                            const columnName = slicerState.targets[0].column;

                            const filter = {{
                                $schema: "http://powerbi.com/product/schema#basic",
                                target: {{
                                    table: tableName,
                                    column: columnName
                                }},
                                operator: "In",
                                values: {slicer.SlicerValue},  // Specify the slicer value here
                                filterType: models.FilterType.BasicFilter
                            }};
                            await visual.setSlicerState({{ filters: [filter] }});
                        }}
                    """

            else:
                slicerContent = ""

            # JavaScript code to embed Power BI report
            js_code = f"""
            () => {{
                var models = window["powerbi-client"].models;
                var reportContainer = document.createElement('div');
                reportContainer.id = 'reportContainer';
                reportContainer.style.width = '800px';
                reportContainer.style.height = '600px';
                document.body.appendChild(reportContainer);

                var reportLoadConfig = {{
                    type: "report",
                    tokenType: models.TokenType.Embed,
                    accessToken: "{embedToken}",
                    embedUrl: "{embedUrl}",
                    settings: {{
                        zoomLevel: 0.54,
                        navContentPaneEnabled: false
                    }},
                }};

                var report = powerbi.embed(reportContainer, reportLoadConfig);

                return new Promise((resolve) => {{
                    report.on("loaded", function() {{

                        report.getPages().then(async pages => {{
                            const selectedPage = pages.find(p => p.name === "{pageName}");
                            if (selectedPage) {{
                            selectedPage.setActive();

                            
                            selectedPage.getVisuals().then(async visuals => {{
                                const dataToReturn = [];  
                                for (let visual of visuals) {{
                                      {slicerContent}
                                    try {{           
                                    const data = await visual.exportData(models.ExportDataType.Summarized);
                                    const visualFilter = await visual.getFilters();
                                    if (visual.type === "slicer" || visual.type === "advancedSlicerVisual") {{
                                        const slicerState = await visual.getSlicerState();
                                        const tableName = slicerState.targets[0].table;
                                        const columnName = slicerState.targets[0].column;
                                        let selectedValues = [];
                                        try {{
                                            selectedValues = slicerState.filters[0].values || [];
                                        }} catch (error) {{
                                            selectedValues = []; // Default to an empty array if any exception occurs
                                        }}

                                        dataToReturn.push({{
                                            Id: visual.name,
                                            Type: visual.type,
                                            Title: visual.title,
                                            VisualData: data,
                                            TableName : tableName,
                                            ColumnName : columnName,
                                            slicerState : slicerState,
                                            selectedValue : selectedValues
                                        }});
                                    }} else{{
                                    dataToReturn.push({{
                                        Id: visual.name,
                                        Type: visual.type,
                                        Title: visual.title,
                                        VisualData: data
                                        
                                
                                    }});
                                    }}
                                    }} catch (error) {{
                                        console.error("error");
                                    }}
                                    
                                }}
                                

                                resolve({{
                                    data: dataToReturn
                                }});
                                

                            }}).catch(error => {{
                             console.error('Error retrieving visuals:', error);
                                resolve("Error1null");  // Resolve with null on error
                            }});
                        }} else {{
                                resolve("Error2null");  // If no page is found, resolve with null
                            }}
                        }}).catch(error => {{
                            console.error('Error retrieving pages:', error);
                            resolve("Error3null");  // Resolve with null on error
                        }});
                    }});

                    report.on("rendered", function () {{
                        console.log("Report render successful");
                    }});
                }});
            }}
            """
            # Evaluate the JS code
            pagesdata = page.evaluate(js_code)
            browser.close()

            # with open("temporaryData/page1Visual.json", "w") as file:
            #     json.dump(pagesdata, file, indent=4)

            return formatData(pagesdata)
        
    except Exception as ex:
        message = f"Error occur at visualExtraction: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
