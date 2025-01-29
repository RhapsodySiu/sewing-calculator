
type Spec = {
    width: number;
    height: number;
    thickness: number;
    roundness: number;
    seamAllowance: number;
    name: string;
};

export async function getPdf(spec: Spec): Promise<void> {
  try {
    const response = await fetch('/api/pdf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(spec),
    });
    if (!response.ok) {
      console.error(`Error: ${response.status} ${response.statusText}`);
      throw new Error(`Failed to fetch PDF: ${response.status}`);
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pattern.pdf';
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('An error occurred while fetching the PDF:', error);
    throw error;
  }
}
