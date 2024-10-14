import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.awt.FontFormatException;

public class ResumeAnalyzerUI {

    public static void main(String[] args) {

        Font museoSans = loadMuseoSansFont();


        JFrame frame = new JFrame("Java Resume Analyzer");
        frame.setSize(600, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null); // Center window

        // Set the top icon
        Image icon = Toolkit.getDefaultToolkit().getImage("Assets/resume.jpg"); // Replace with the path to your icon
        frame.setIconImage(icon);


        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout(10, 10));
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));


        JLabel fileLabel = new JLabel("Upload your resume PDF:");
        fileLabel.setFont(museoSans.deriveFont(14f));
        panel.add(fileLabel, BorderLayout.NORTH);


        JButton uploadButton = new JButton("Upload Resume");
        uploadButton.setPreferredSize(new Dimension(150, 30)); // Smaller button
        panel.add(uploadButton, BorderLayout.CENTER);


        JPanel centerPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        centerPanel.setBorder(BorderFactory.createEmptyBorder(20, 0, 20, 0));
        centerPanel.add(uploadButton);
        panel.add(centerPanel, BorderLayout.CENTER);


        JTextArea resultArea = new JTextArea();
        resultArea.setFont(museoSans.deriveFont(12f)); // Set Museo Sans 300 font
        resultArea.setEditable(false);
        resultArea.setLineWrap(true);
        resultArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(resultArea);
        scrollPane.setPreferredSize(new Dimension(580, 200));
        panel.add(scrollPane, BorderLayout.SOUTH);


        uploadButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setDialogTitle("Select Your PDF Resume");
                fileChooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter("PDF Files", "pdf"));

                int result = fileChooser.showOpenDialog(null);

                if (result == JFileChooser.APPROVE_OPTION) {
                    File selectedFile = fileChooser.getSelectedFile();
                    String resumeText = ResumeReader.extractTextFromPDF(selectedFile.getAbsolutePath());

                    if (resumeText.startsWith("Error")) {
                        resultArea.setText("Error: " + resumeText);
                        return;
                    }

                    String analysisResult = analyzeResumeWithPython(resumeText);
                    if (analysisResult.startsWith("Error")) {
                        resultArea.setText(analysisResult);
                    } else {
                        resultArea.setText(formatAnalysisResult(analysisResult)); // Format results here
                    }
                } else {
                    resultArea.setText("No file selected.");
                }
            }
        });


        frame.add(panel);
        frame.setVisible(true);
    }


    private static Font loadMuseoSansFont() {
        try {
            File fontFile = new File("Assets/museo-sans-300.ttf");
            Font museoSans = Font.createFont(Font.TRUETYPE_FONT, new FileInputStream(fontFile));
            return museoSans;
        } catch (FontFormatException | IOException e) {
            System.err.println("Font loading failed: " + e.getMessage());
            return new Font("SansSerif", Font.PLAIN, 12); // Fallback to default font
        }
    }


    public static String analyzeResumeWithPython(String resumeText) {
        StringBuilder output = new StringBuilder();

        // Specify the path to the analyze_resume.exe directly, since it's in the same folder as this code
        String scriptPath = "analyze_resume.exe"; // Adjust this based on your project structure

        ProcessBuilder processBuilder = new ProcessBuilder(scriptPath);
        processBuilder.redirectErrorStream(true);  // Combine stdout and stderr

        try {
            Process process = processBuilder.start();

            // Write resume text to process input
            try (var outputStream = process.getOutputStream()) {
                byte[] utf8Bytes = resumeText.getBytes("UTF-8");  // Encode as UTF-8
                outputStream.write(utf8Bytes);
                outputStream.flush();
            }

            // Read process output
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                }
            }

            // Wait for process to complete and check exit code
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                return "Error during analysis. Exit code: " + exitCode + "\n" + output.toString().trim();
            }

        } catch (IOException | InterruptedException e) {
            return "Error during analysis: " + e.getMessage();
        }

        return output.toString().trim();
    }


    public static String formatAnalysisResult(String result) {

        result = result.replaceAll("(Experience|Skills|Education|Certifications)", "**$1**");
        return result;
    }
}
