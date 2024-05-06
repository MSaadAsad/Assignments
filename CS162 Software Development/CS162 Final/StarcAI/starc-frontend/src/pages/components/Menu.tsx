import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/router";
import Image from "next/image";
import styles from "../../styles/Menu.module.css"; // Adjust the path to your CSS module
import axios from "axios";

//importing icons
import HomeIcon from "../../assets/home.svg"; // Adjust the path according to your assets folder structure
import AccountIcon from "../../assets/account.svg";
import SettingsIcon from "../../assets/settings.svg";
import DocumentIcon from "../../assets/document.svg";
import CloseIcon from "../../assets/close.svg";
import MenuIcon from "../../assets/menu.svg";
import UploadIcon from "../../assets/upload.svg";

const Menu = ({ defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const router = useRouter();
  const [isNewDocModalOpen, setIsNewDocModalOpen] = useState(false);
  const [newDocTitle, setNewDocTitle] = useState("");
  const [newDocText, setNewDocText] = useState("");

  const documentId = router.query.documentId; // Capturing the document ID from the URL

  // Log the document ID to the console for debugging
  useEffect(() => {
    console.log("Document ID:", documentId);
  }, [documentId]);

  const modalRef = useRef<HTMLDivElement | null>(null);

  const createNewDocument = async () => {
    const authToken = localStorage.getItem("authToken");
    try {
      const response = await axios.post(
        "https://starcai.onrender.com/docs",
        {
          title: newDocTitle,
          text: newDocText,
        },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        },
      );

      if (response.status === 200) {
        const newDocId = response.data.id;
        setIsNewDocModalOpen(false); // Close the modal
        router.push(`/home/${newDocId}`); // Navigate to the new document's page
      } else {
        // Handle other status codes appropriately
      }
    } catch (error) {
      console.error("Error creating new document:", error);
      // Handle error appropriately
    }
  };
  // Time delay to match the transition duration of the menu
  useEffect(() => {
    if (!defaultOpen) {
      if (isOpen) {
        const timer = setTimeout(() => setAnimationCompleted(true), 300);
        return () => clearTimeout(timer);
      } else {
        setAnimationCompleted(false);
      }
    }
  }, [isOpen, defaultOpen]);

  const toggleMenu = () => setIsOpen(!isOpen);

  const handleLogout = async () => {
    const authToken = localStorage.getItem("authToken");

    if (authToken) {
      try {
        const response = await axios.post(
          "https://starcai.onrender.com/auth/logout",
          {},
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          },
        );

        console.log("Logout successful:", response.data);
        localStorage.removeItem("authToken"); // Remove the token from storage
        router.push("/login"); // Redirect to the login page
      } catch (error) {
        console.error("Logout failed:", error);
        // Optionally show an error message to the user
      }
    } else {
      console.error("No auth token found");
    }
  };

  const exportDocumentAsPdf = async (documentId: string) => {
    const authToken = localStorage.getItem("authToken");

    if (!authToken) {
      console.error("No auth token found");
      return;
    }

    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/docs/pdf/${documentId}`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
          responseType: "blob", // Important for handling binary data
        },
      );

      // Create a URL for the blob
      const fileURL = window.URL.createObjectURL(new Blob([response.data]));
      const fileLink = document.createElement("a");

      fileLink.href = fileURL;
      fileLink.setAttribute("download", "document.pdf"); // Set the file name
      document.body.appendChild(fileLink);

      fileLink.click(); // Programmatically click the link to trigger the download
      fileLink.remove(); // Clean up the DOM
    } catch (error) {
      console.error("Error exporting document", error);
      // Optionally show an error message to the user
    }
  };

  const navigateTo = (path: string) => {
    // Check if the current path contains '/docs'
    if (router.pathname.includes("/docs") && path === "/docs") {
      // If already on a '/docs' page, do nothing
      return;
    }

    setIsOpen(false); // Close the menu when a link is clicked
    router.push(path); // Programmatically navigate to the path
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const [animationCompleted, setAnimationCompleted] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        setAnimationCompleted(true);
      }, 300); // Delay to match the transition duration

      return () => clearTimeout(timer);
    } else {
      setAnimationCompleted(false); // Immediately set to false when closing
    }
  }, [isOpen]);

  const onTransitionEnd = () => {
    if (isOpen) {
      setAnimationCompleted(true); // Set to true once the opening transition ends
    }
  };

  const uploadFile = async () => {
    const formData = new FormData();
    if (selectedFile) {
      formData.append("pdf", selectedFile, selectedFile.name);
    }

    try {
      const authToken = localStorage.getItem("authToken");
      const response = await axios.post(
        "https://starcai.onrender.com/docs/pdf",
        formData,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        },
      );
      console.log("File uploaded successfully", response.data);
      setIsUploadModalOpen(false); // Close the modal after upload
    } catch (error) {
      console.error("Error uploading file", error);
    }
  };

  return (
    <>
      {/* Menu Toggle Button */}
      {!defaultOpen && (
        <button
          onClick={toggleMenu}
          className="absolute left-0 top-0 z-30 rounded-full p-2 transition duration-300 hover:bg-gray-200"
        >
          <div className="relative">
            {isOpen ? (
              <div> </div>
            ) : (
              <Image src={MenuIcon} alt="Menu" width={42} height={42} />
            )}
          </div>
        </button>
      )}

      {/* Menu Overlay */}
      <div
        className={`fixed inset-y-0 left-0 z-20 transition-transform duration-300 ${
          !defaultOpen ? (isOpen ? "translate-x-0" : "-translate-x-full") : ""
        } ${
          animationCompleted && !defaultOpen ? "bg-gray-800 bg-opacity-75" : ""
        } ${!defaultOpen ? (defaultOpen ? "right-1/4" : "right-0") : ""}`}
        onTransitionEnd={onTransitionEnd}
      >
        {/* Menu Items Container */}
        <div className="fixed inset-y-0 left-0 z-30 w-full max-w-xs overflow-y-auto border-r-2 border-gray-300 bg-white p-5">
          {/* Navigation Links */}
          <nav className="flex flex-col space-y-5">
            <button
              onClick={() => navigateTo("/docs")}
              className={`flex items-center space-x-2 rounded-md bg-white px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300 ${styles.menuItem}`}
            >
              <Image src={HomeIcon} alt="Home" width={24} height={24} />
              <span>Home</span>
            </button>
            <button
              onClick={() => navigateTo("/not-found")}
              className={`flex items-center space-x-2 rounded-md bg-white px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300 ${styles.menuItem}`}
            >
              <Image src={AccountIcon} alt="Account" width={24} height={24} />
              <span>Account</span>
            </button>
            <button
              onClick={() => navigateTo("/not-found")}
              className={`flex items-center space-x-2 rounded-md bg-white px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300 ${styles.menuItem}`}
            >
              <Image src={SettingsIcon} alt="Settings" width={24} height={24} />
              <span>Settings</span>
            </button>

            {/* New Document Modal */}
            {isNewDocModalOpen && (
              <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-600 bg-opacity-50">
                <div className="relative rounded bg-white p-5">
                  <h2 className="text-lg">Create New Document</h2>
                  <input
                    type="text"
                    placeholder="Document Title"
                    value={newDocTitle}
                    onChange={(e) => setNewDocTitle(e.target.value)}
                    className="mt-2 w-full rounded border p-2"
                  />
                  <textarea
                    placeholder="Document Content"
                    value={newDocText}
                    onChange={(e) => setNewDocText(e.target.value)}
                    className="mt-2 w-full rounded border p-2"
                    rows={4}
                  />
                  <div className="mt-4 flex justify-end">
                    <button
                      onClick={() => setIsNewDocModalOpen(false)}
                      className="mr-2 rounded bg-gray-300 px-4 py-2 text-black"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={createNewDocument}
                      className="rounded bg-blue-500 px-4 py-2 text-white"
                    >
                      Create
                    </button>
                  </div>
                </div>
              </div>
            )}

            <button
              onClick={() => setIsNewDocModalOpen(true)}
              className={`flex items-center space-x-2 rounded-md bg-white px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300 ${styles.menuItem}`}
            >
              <Image
                src={DocumentIcon}
                alt="New Document"
                width={24}
                height={24}
              />
              <span>New document</span>
            </button>
            <button
              onClick={() => setIsUploadModalOpen(true)}
              className={`flex items-center space-x-2 rounded-md bg-gray-200 px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300 ${styles.menuItem}`}
            >
              <Image src={UploadIcon} alt="Upload" width={24} height={24} />
              <span>Upload</span>
            </button>

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 rounded-md bg-white px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300"
            >
              <span>Logout</span> {/* Add an icon if needed */}
            </button>

            <button
              onClick={() => exportDocumentAsPdf(documentId!.toString())}
              className="flex items-center space-x-2 rounded-md bg-white px-4 py-2 text-gray-800 transition-colors duration-200 hover:bg-gray-300"
            >
              {/* Icon and Label for Export Button */}
              <span>Export as PDF</span>
            </button>

            {/* Upload Modal */}
            {isUploadModalOpen && (
              <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-600 bg-opacity-50">
                <div className="relative rounded bg-white p-5">
                  <div className="mb-2 flex items-center justify-between">
                    <h2 className="text-lg">Upload File</h2>
                    <button
                      onClick={() => setIsUploadModalOpen(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <Image
                        src={CloseIcon}
                        alt="Close"
                        width={32}
                        height={32}
                      />
                    </button>
                  </div>
                  {/* Updated file input */}
                  <input
                    type="file"
                    name="pdf"
                    accept=".pdf" // Accept only PDF files if that's the requirement
                    onChange={handleFileChange}
                    className={styles.fileInput} // Apply your CSS styles if needed
                  />
                  <button
                    onClick={uploadFile}
                    className="mt-2 rounded bg-blue-500 px-4 py-2 text-white"
                  >
                    Upload
                  </button>
                </div>
              </div>
            )}
          </nav>
        </div>
      </div>
      {animationCompleted && !defaultOpen && (
        <button
          onClick={toggleMenu}
          className="absolute left-80 top-0 z-40 ml-6 rounded-full bg-white p-2 transition duration-300 hover:bg-gray-200"
        >
          <Image src={CloseIcon} alt="Close" width={32} height={32} />
        </button>
      )}
    </>
  );
};

export default Menu;
